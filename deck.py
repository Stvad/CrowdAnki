from uuid import uuid1
from collections import namedtuple

import CrowdAnki.utils
from CrowdAnki import utils
from CrowdAnki.common_constants import UUID_FIELD_NAME
from CrowdAnki.deck_config import DeckConfig
from CrowdAnki.json_serializable import JsonSerializableAnkiDict
from CrowdAnki.note import Note
from CrowdAnki.note_model import NoteModel


class Deck(JsonSerializableAnkiDict):
    Metadata = namedtuple("DeckMetadata", ["deck_configs", "models"])
    # Todo either unpack or represent differently because right now - not serialized properly

    filter_set = JsonSerializableAnkiDict.filter_set | \
                 {"collection",
                  "newToday",
                  "revToday",
                  "timeToday",
                  "lrnToday",
                  "metadata"}
    # todo super(Deck, self)

    def __init__(self, anki_deck=None):
        super(Deck, self).__init__(anki_deck)
        self.collection = None
        self.name = None
        self.notes = None
        self.children = None
        self.metadata = None

    @classmethod
    def from_collection(cls, collection, name, deck_metadata=None):
        deck = Deck()

        # deck._update_db()
        anki_dict = collection.decks.byName(name)

        deck = Deck(anki_dict)

        deck.collection = collection
        deck.name = name

        deck._update_fields()

        deck.notes = Note.get_notes_from_collection(collection, deck.anki_dict["id"])  # Todo ugly

        deck.metadata = deck_metadata
        deck._load_metadata()

        deck.children = [cls.from_collection(collection, child_name, deck_metadata) for child_name, _ in
                         collection.decks.children(deck.anki_dict["id"])]

        return deck

    def _update_db(self):
        # Introduce uuid field for unique identification of entities
        CrowdAnki.utils.add_column(self.collection.db, "notes", UUID_FIELD_NAME)

    def _load_metadata(self):
        if not self.metadata:
            self.metadata = Deck.Metadata({}, {})

        self._load_deck_config()
        self._load_note_models()

    def _load_deck_config(self):
        # Todo switch to uuid
        new_config = DeckConfig.from_collection(self.collection, self.anki_dict["conf"])
        # config_uiid = new_config.anki_dict[UUID_FIELD_NAME]

        self.metadata.deck_configs.setdefault(new_config.get_uuid(), new_config)

    def _load_note_models(self):
        for note in self.notes:
            note_model = NoteModel.from_collection(self.collection, note.anki_object.mid)
            self.metadata.models.setdefault(note_model.get_uuid(), note_model)

    def _dict_extension(self):
        return utils.merge_dicts(
            super(Deck, self)._dict_extension(),
            {"note_models": self.metadata.models.values(),
             "deck_configurations": self.metadata.deck_configs.values()})
