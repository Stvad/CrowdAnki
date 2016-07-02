import json

from representation.deck import Deck


class AnkiJsonImporter(object):
    def __init__(self, collection):
        self.collection = collection

    def load_from_file(self, file_path):
        deck = None
        with open(file_path) as deck_file:
            # deck_json = json.load(deck_file, object_hook=JsonSerializable.json_object_hook)
            deck_json = json.load(deck_file)
            deck = Deck.from_json(deck_json)
            deck.save_to_collection(self.collection)
