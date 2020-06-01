from anki import Collection
from .json_serializable import JsonSerializableAnkiDict
from ..utils.uuid import UuidFetcher


class DeckConfig(JsonSerializableAnkiDict):
    def __init__(self, anki_deck_config=None):
        super(DeckConfig, self).__init__(anki_deck_config)

    @classmethod
    def from_collection(cls, collection, deck_config_id):
        anki_dict = collection.decks.getConf(deck_config_id)
        deck_config = DeckConfig(anki_dict)
        deck_config._update_fields()

        return deck_config

    def save_to_collection(self, collection: Collection):
        # Todo whole uuid matching thingy
        # For now only create scenario

        config_dict = self.fetch_or_create_config(collection)

        config_dict.update(self.anki_dict)
        collection.decks.update_config(config_dict)

        self.anki_dict = config_dict

    def fetch_or_create_config(self, collection):
        return UuidFetcher(collection).get_deck_config(self.get_uuid()) or \
               collection.decks.add_config(self.anki_dict["name"])
