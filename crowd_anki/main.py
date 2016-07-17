import os.path
from pprint import pprint
from pathlib import Path

from crowd_anki import anki_exporter_wrapper  # To hook exporters list extension
from crowd_anki.anki_importer import AnkiJsonImporter
from crowd_anki.anki_exporter import AnkiJsonExporter

import aqt.utils
from anki import Collection
from aqt import mw, QAction, QFileDialog

COLLECTION_PATH = "../../WCollection/collection.anki2"


def main():
    deck_name = "tdeckl1"
    collection = Collection(COLLECTION_PATH)
    print(os.path.realpath(os.path.curdir))

    exporter = AnkiJsonExporter(collection)
    exporter.export_deck_to_directory(deck_name)

    # deck_directory = os.path.join("./", deck_name)
    deck_directory = Path(deck_name)
    # deck_json = os.path.join(deck_directory, deck_name + ".json")

    # importer = AnkiJsonImporter(collection)
    # importer.load_from_directory(deck_directory)

    collection.close()


def on_import_action():
    directory_path = str(QFileDialog.getExistingDirectory(caption="Select Deck Directory"))
    if not directory_path:
        return

    exported_directory = Path(directory_path)

    importer = AnkiJsonImporter(mw.col)
    importer.load_from_directory(exported_directory)

    aqt.utils.showInfo("Import of {} deck was successful".format(exported_directory.name))


def anki_import_init():
    import_action = QAction("Import CrowdAnki Json", mw)
    import_action.triggered.connect(on_import_action)

    # -2 supposed to give the separator after import/export section, so button should be at the end of this section
    mw.form.menuCol.insertActions(mw.form.menuCol.actions()[-2], [import_action])


def anki_init():
    anki_import_init()


if __name__ == "__main__":
    main()
else:
    anki_init()

"""
Warning:
Creation of collection has a side effect of changing current directory to ${collection_path}/collection.media
"""
