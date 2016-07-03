import os.path
from pprint import pprint

from anki_importer import AnkiJsonImporter
from anki_exporter import AnkiJsonExporter

from anki import Collection
from anki.notes import Note as AnkiNote

COLLECTION_PATH = "../../WCollection/collection.anki2"


def main():
    deck_name = "tdeckl1"
    collection = Collection(COLLECTION_PATH)
    print(os.path.realpath(os.path.curdir))

    exporter = AnkiJsonExporter(collection)
    exporter.export_deck(deck_name)

    deck_directory = os.path.join("./", deck_name)
    deck_json = os.path.join(deck_directory, deck_name + ".json")

    importer = AnkiJsonImporter(collection)
    importer.load_from_file(deck_json)

    collection.close()


def anki_init():
    pass


if __name__ == "__main__":
    main()
else:
    anki_init()


"""
Warning:
Creation of collection has a side effect of changing current directory to ${collection_path}/collection.media
"""
