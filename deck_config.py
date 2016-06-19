from uuid import uuid1

from CrowdAnki.common_constants import UUID_FIELD_NAME
from CrowdAnki.json_serializable import JsonSerializable


class DeckConfig(JsonSerializable):
    def __init__(self):
        super(DeckConfig, self).__init__()
        self.anki_deck_config = None

    @classmethod
    def from_collection(cls, collection, deck_config_id):
        deck_config = DeckConfig()
        deck_config.anki_deck_config = collection.decks.getConf(deck_config_id)
        deck_config._update_fields()

        return deck_config

    def _update_fields(self):
        self.anki_deck_config.setdefault(UUID_FIELD_NAME, str(uuid1()))

    def _dict_extension(self):
        return self.anki_deck_config