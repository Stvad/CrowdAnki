from uuid import uuid1

from CrowdAnki.common_constants import UUID_FIELD_NAME
from CrowdAnki.json_serializable import JsonSerializableAnkiDict


class DeckConfig(JsonSerializableAnkiDict):
    # filter_set = JsonSerializableAnkiDict.filter_set | {}

    def __init__(self, anki_deck_config=None):
        super(DeckConfig, self).__init__(anki_deck_config)

    @classmethod
    def from_collection(cls, collection, deck_config_id):
        deck_config = DeckConfig()
        deck_config.anki_dict = collection.decks.getConf(deck_config_id)
        deck_config._update_fields()

        return deck_config

