from uuid import uuid1
from collections import namedtuple

import CrowdAnki.utils
from CrowdAnki.common_constants import UUID_FIELD_NAME
from CrowdAnki.deck_config import DeckConfig
from CrowdAnki.json_serializable import JsonSerializableAnkiDict
from CrowdAnki.note import Note


class Deck(JsonSerializableAnkiDict):
    Metadata = namedtuple("DeckMetadata", ["deck_configs", "models"])
    filter_set = JsonSerializableAnkiDict.filter_set | {"collection"}
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
        deck.collection = collection
        deck.name = name

        # deck._update_db()
        deck.anki_dict = collection.decks.byName(name)
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
        config_uiid = new_config.anki_dict[UUID_FIELD_NAME]

        self.metadata.deck_configs.setdefault(config_uiid, new_config)

    def _load_note_models(self):
        pass
