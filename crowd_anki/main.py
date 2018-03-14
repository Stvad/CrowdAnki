from .thirdparty.pathlib import Path

from crowd_anki import anki_exporter_wrapper  # Do not remove. To hook exporters list extension
from crowd_anki.anki_importer import AnkiJsonImporter
from crowd_anki.github.github_importer import GithubImporter

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

    import_directory = Path(directory_path)
    AnkiJsonImporter.import_deck(aqt.mw.col, import_directory)


def anki_import_init():
    import_action = QAction("CrowdAnki: Import from disk", mw)
    import_action.triggered.connect(on_import_action)

    github_import_action = QAction("CrowdAnki: Import from Github", mw)
    github_import_action.triggered.connect(lambda : GithubImporter.on_github_import_action(mw.col))

    # -2 supposed to give the separator after import/export section, so button should be at the end of this section
    mw.form.menuCol.insertActions(mw.form.menuCol.actions()[-2], [import_action, github_import_action])


def anki_init():
    if mw:
        anki_import_init()


if __name__ == "__main__":
    main()
else:
    anki_init()

"""
Warning:
Creation of collection has a side effect of changing current directory to ${collection_path}/collection.media
"""
