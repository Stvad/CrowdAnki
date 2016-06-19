class DeckConfig(object):
    def __init__(self):
        pass

    def from_collection(self, collection, deck_config_id):
        self.anki_deck_config = collection.decks.getConf(deck_config_id)