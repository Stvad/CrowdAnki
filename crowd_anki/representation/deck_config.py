from .json_serializable import JsonSerializableAnkiDict


class DeckConfig(JsonSerializableAnkiDict):
    def __init__(self, anki_deck_config=None):
        super(DeckConfig, self).__init__(anki_deck_config)

    @classmethod
    def from_collection(cls, collection, deck_config_id):
        anki_dict = collection.decks.getConf(deck_config_id)
        deck_config = DeckConfig(anki_dict)
        deck_config._update_fields()

        return deck_config

    def save_to_collection(self, collection):
        # Todo whole uuid matching thingy
        # For now only create scenario

        config_dict = collection.decks.get_deck_config_by_uuid(self.get_uuid())

        if config_dict:
            config_dict.update(self.anki_dict)
        else:
            new_id = collection.decks.confId(self.anki_dict["name"], self.anki_dict)
            config_dict = collection.decks.getConf(new_id)

        self.anki_dict = config_dict

        collection.decks.save()
        collection.decks.flush()
