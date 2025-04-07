import anki
import anki.utils
from anki.notes import Note as AnkiNote
from .json_serializable import JsonSerializableAnkiObject
from .note_model import NoteModel
from ..anki.overrides.change_model_dialog import ChangeModelDialog
from ..importer.import_dialog import ImportConfig
from ..config.config_settings import ConfigSettings
from ..utils.constants import UUID_FIELD_NAME
from ..utils.uuid import UuidFetcher


class Note(JsonSerializableAnkiObject):
    export_filter_set = JsonSerializableAnkiObject.export_filter_set | \
                        {"col",  # Don't need collection
                         "_fmap",  # Generated data
                         "_model",  # Card model. Would be handled by deck.
                         "mid",  # -> uuid
                         "scm",  # todo: clarify
                         "config",
                         "newlyAdded"
                         }

    def __init__(self, anki_note=None, config: ConfigSettings = None):
        super(Note, self).__init__(anki_note)
        self.note_model_uuid = None
        self.config = config or ConfigSettings.get_instance()

    @staticmethod
    def get_notes_from_collection(collection, deck_id, note_models):
        note_ids = collection.decks.get_note_ids(deck_id, include_from_dynamic=True)
        return [Note.from_collection(collection, note_id, note_models) for note_id in note_ids]

    @classmethod
    def from_collection(cls, collection, note_id, note_models):
        anki_note = AnkiNote(collection, id=note_id)
        note = Note(anki_note=anki_note)

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

    def note_type(self):
        # TODO Remove compatibility shims for Anki 2.1.46 and lower.
        # (Remove this method altogether — see old version in git
        # history.)
        return self.anki_object.note_type() if hasattr(self.anki_object, 'note_type') else self.anki_object.model()

    def handle_model_update(self, collection, model_map_cache):
        """
        Update note's cards if note's model has changed
        """
        old_model_uuid = self.note_type().get(UUID_FIELD_NAME)
        if self.note_model_uuid == old_model_uuid:
            return

        # todo if models semantically identical - create map without calling dialog

        uuid_fetcher = UuidFetcher(collection)
        new_model = NoteModel.from_json(uuid_fetcher.get_model(self.note_model_uuid))
        mapping = model_map_cache[old_model_uuid].get(self.note_model_uuid)
        if mapping:
            collection.models.change(self.note_type(),
                                     [self.anki_object.id],
                                     new_model.anki_dict,
                                     mapping.field_map,
                                     mapping.template_map)
        else:
            new_model.make_current(collection)
            # todo signals instead of direct dialog creation?
            dialog = ChangeModelDialog(collection, [self.anki_object.id], self.note_type())

            def on_accepted():
                model_map_cache[old_model_uuid][self.note_model_uuid] = \
                    NoteModel.ModelMap(dialog.get_field_map(), dialog.get_template_map())

            dialog.accepted.connect(on_accepted)
            dialog.exec()
            # todo process cancel

        # To get an updated note to work with
        self.anki_object = uuid_fetcher.get_note(self.get_uuid())

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

    def save_to_collection(self, collection, deck, model_map_cache, import_config):
        # Todo uuid match on existing notes

        note_model = deck.metadata.models[self.note_model_uuid]

        self.anki_object = UuidFetcher(collection).get_note(self.get_uuid())
        new_note = self.anki_object is None
        if new_note:
            self.anki_object = AnkiNote(collection, note_model.anki_dict)
        else:
            self.handle_model_update(collection, model_map_cache)

        self.handle_import_config_changes(import_config, note_model)

        self.anki_object.__dict__.update(self.anki_object_dict)
        self.anki_object.mid = note_model.anki_dict["id"]
        self.anki_object.mod = anki.utils.int_time()

        if new_note:
            collection.add_note(self.anki_object, deck.anki_dict["id"])
        else:
            collection.update_note(self.anki_object, skip_undo_entry=True)
            if not import_config.ignore_deck_movement:
                self.move_cards_to_deck(deck.anki_dict["id"])

    def handle_import_config_changes(self, import_config, note_model):
        # Personal Fields
        for num in range(len(self.anki_object_dict["fields"])):
            if import_config.is_personal_field(note_model.anki_dict['name'], note_model.anki_dict['flds'][num]['name']):
                self.anki_object_dict["fields"][num] = self.anki_object.fields[num]

        # Tag Cards on Import
        self.anki_object_dict["tags"] += import_config.add_tag_to_cards
