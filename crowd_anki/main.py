import os.path
from pprint import pprint
from pathlib import Path

from crowd_anki.anki_importer import AnkiJsonImporter
from crowd_anki.anki_exporter import AnkiJsonExporter

from anki import Collection
from aqt import mw, QAction

COLLECTION_PATH = "../../WCollection/collection.anki2"


def main():
    deck_name = "tdeckl1"
    collection = Collection(COLLECTION_PATH)
    print(os.path.realpath(os.path.curdir))

    # exporter = AnkiJsonExporter(collection)
    # exporter.export_deck(deck_name)

    # deck_directory = os.path.join("./", deck_name)
    deck_directory = Path(deck_name)
    # deck_json = os.path.join(deck_directory, deck_name + ".json")

    importer = AnkiJsonImporter(collection)
    importer.load_from_directory(deck_directory)

    collection.close()


def test_import():
    exported_directory = \
        Path("/usermedia/Cloud/Dropbox/SoftwareEngineering/Projects/Anki/WCollection/collection.media/tdeckl1")
    importer = AnkiJsonImporter(mw.col)
    importer.load_from_directory(exported_directory)


def anki_init():
    action = QAction("test_import_ca", mw)
    action.triggered.connect(test_import)
    mw.form.menuTools.addAction(action)


if __name__ == "__main__":
    main()
else:
    anki_init()



"""
Warning:
Creation of collection has a side effect of changing current directory to ${collection_path}/collection.media
"""
