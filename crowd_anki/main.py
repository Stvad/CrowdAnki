from pathlib2 import Path

from crowd_anki import anki_exporter_wrapper  # To hook exporters list extension
from crowd_anki.anki_importer import AnkiJsonImporter

import aqt.utils
from aqt import mw, QAction, QFileDialog


def main():
    """
    Todo: Implement command line interface
    """


def on_import_action():
    directory_path = str(QFileDialog.getExistingDirectory(caption="Select Deck Directory"))
    if not directory_path:
        return

    exported_directory = Path(directory_path)

    importer = AnkiJsonImporter(mw.col)
    try:
        importer.load_from_directory(exported_directory)

        aqt.utils.showInfo("Import of {} deck was successful".format(exported_directory.name))
    except ValueError as error:
        aqt.utils.showWarning(error.args[0])


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
