import anki
import anki.utils
from anki.notes import Note as AnkiNote

try:
    from crowd_anki.anki_overrides.change_model_dialog import ChangeModelDialog
except ImportError:
    # need this to decouple it from pyqt. To simplify running of the tests with Travis
    print("Failed to import ChangeModelDialog")

from ..utils.constants import UUID_FIELD_NAME
from .json_serializable import JsonSerializableAnkiObject
from .note_model import NoteModel


class Note(JsonSerializableAnkiObject):
    export_filter_set = JsonSerializableAnkiObject.export_filter_set | \
                        {"col",  # Don't need collection
                         "_fmap",  # Generated data
                         "_model",  # Card model. Would be handled by deck.
                         "mid",  # -> uuid
                         "scm"  # todo: clarify
                         }

    def __init__(self, anki_note=None):
        super(Note, self).__init__(anki_note)
        self.note_model_uuid = None

    @staticmethod
    def get_notes_from_collection(collection, deck_id, note_models):
        note_ids = collection.decks.get_note_ids(deck_id, include_from_dynamic=True)
        return [Note.from_collection(collection, note_id, note_models) for note_id in note_ids]

    @classmethod
    def from_collection(cls, collection, note_id, note_models):
        anki_note = AnkiNote(collection, id=note_id)
        note = Note(anki_note)

        note_model = NoteModel.from_collection(collection, note.anki_object.mid)
        note_models.setdefault(note_model.get_uuid(), note_model)

        note.note_model_uuid = note_model.get_uuid()

        return note

    @classmethod
    def from_json(cls, json_dict):
        note = Note()
        note.anki_object_dict = json_dict
        note.note_model_uuid = json_dict["note_model_uuid"]
        return note

    def get_uuid(self):
        return self.anki_object.guid if self.anki_object else self.anki_object_dict.get("guid")

    def handle_model_update(self, collection, model_map_cache):
        """
        Update note's cards if note's model has changed
        """
        old_model_uuid = self.anki_object.model().get(UUID_FIELD_NAME)
        if self.note_model_uuid == old_model_uuid:
            return

        # todo if models semantically identical - create map without calling dialog

        new_model = NoteModel.from_json(collection.models.get_by_uuid(self.note_model_uuid))
        mapping = model_map_cache[old_model_uuid].get(self.note_model_uuid)
        if mapping:
            collection.models.change(self.anki_object.model(),
                                     [self.anki_object.id],
                                     new_model.anki_dict,
                                     mapping.field_map,
                                     mapping.template_map)
        else:
            new_model.make_current(collection)
            # todo signals instead of direct dialog creation?
            dialog = ChangeModelDialog(collection, [self.anki_object.id], self.anki_object.model())

            def on_accepted():
                model_map_cache[old_model_uuid][self.note_model_uuid] = \
                    NoteModel.ModelMap(dialog.get_field_map(), dialog.get_template_map())

            dialog.accepted.connect(on_accepted)
            dialog.exec_()
            # todo process cancel

        # To get an updated note to work with
        self.anki_object = AnkiNote.get_by_uuid(collection, self.get_uuid())

    def move_cards_to_deck(self, deck_id, move_from_dynamic_decks=False):
        """
        Move all cards for note with given id to specified deck.
        :param deck_id:
        :param move_from_dynamic_decks:
        :return:
        """
        # Todo: consider move only when majority of cards are in a different deck.
        for card in self.anki_object.cards():
            card.move_to_deck(deck_id, move_from_dynamic_decks)
            card.flush()

    def save_to_collection(self, collection, deck, model_map_cache):
        # Todo uuid match on existing notes

        note_model = deck.metadata.models[self.note_model_uuid]
        # You may ask WTF? Well, it seems anki has 2 ways to identify deck where to place card:
        # 1) Looking for existing cards of this note
        # 2) Looking at model->did and to add new cards to correct deck we need to modify the did each time
        # ;(
        note_model.anki_dict["did"] = deck.anki_dict["id"]

        self.anki_object = AnkiNote.get_by_uuid(collection, self.get_uuid())
        new_note = self.anki_object is None
        if new_note:
            self.anki_object = AnkiNote(collection, note_model.anki_dict)
        else:
            self.handle_model_update(collection, model_map_cache)

        self.anki_object.__dict__.update(self.anki_object_dict)
        self.anki_object.mid = note_model.anki_dict["id"]
        self.anki_object.mod = anki.utils.intTime()
        self.anki_object.flush()

        if new_note:
            collection.addNote(self.anki_object)
        else:
            self.move_cards_to_deck(deck.anki_dict["id"])
