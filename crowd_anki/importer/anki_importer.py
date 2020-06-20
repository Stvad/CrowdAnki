import json
import os
import shutil
from pathlib import Path
from typing import Callable, Optional

import aqt
import aqt.utils
import yaml

from ..representation import deck_initializer
from ..utils.constants import DECK_FILE_NAME, DECK_FILE_EXTENSION, MEDIA_SUBDIRECTORY_NAME, IMPORT_CONFIG_NAME, \
    CONFIG_EXTENSION
from ..importer.import_dialog import ImportDialog, ImportConfig
from aqt.qt import QDialog


class AnkiJsonImporter:
    def __init__(self, collection, deck_file_name: str = DECK_FILE_NAME):
        self.collection = collection
        self.deck_file_name = deck_file_name

    def load_deck(self, deck_json, directory_path, import_config: ImportConfig):
        """
        Load deck serialized to directory
        Assumes that deck json file is located in the directory
        and named 'deck.json'
        :param deck_json: The deck json dictionary
        :param directory_path: Path
        :param import_config: Config data chosen by the user
        """
        if aqt.mw:
            aqt.mw.backup()

        try:
            deck = deck_initializer.from_json(deck_json, import_config=import_config)
            deck.save_to_collection(self.collection)

            if import_config.use_media:
                media_directory = directory_path.joinpath(MEDIA_SUBDIRECTORY_NAME)
                if media_directory.exists():
                    unicode_media_directory = str(media_directory)
                    src_files = os.listdir(unicode_media_directory)
                    for filename in src_files:
                        full_filename = os.path.join(unicode_media_directory, filename)
                        if os.path.isfile(full_filename):
                            shutil.copy(full_filename, self.collection.media.dir())
                else:
                    print("Warning: no media directory exists.")
        finally:
            if aqt.mw:
                aqt.mw.deckBrowser.show()

    def get_deck_path(self, directory_path):
        """
        Provides compatibility layer between deck file naming conventions.
        Assumes that deck json file is located in the directory and named 'deck.json'
        """

        def path_for_name(name):
            return directory_path.joinpath(name).with_suffix(DECK_FILE_EXTENSION)

        convention_path = path_for_name(self.deck_file_name)   # [folder]/deck.json
        inferred_path = path_for_name(directory_path.name)     # [folder]/[folder].json
        return convention_path if convention_path.exists() else inferred_path

    def load_deck_with_settings(self, directory_path) -> (dict, ImportConfig):
        deck_json = self.read_deck(self.get_deck_path(directory_path))
        import_config = self.read_import_config(directory_path)

        import_dialog = ImportDialog(deck_json, import_config)
        if import_dialog.exec_() == QDialog.Rejected:
            return None, None  # User has cancelled

        # TODO: strip settings from deck_json

        return deck_json, import_dialog.final_import_config

    @staticmethod
    def read_deck(file_path: Path):
        if not file_path.exists():
            raise ValueError("There is no {} file inside of the selected directory".format(file_path))

        with file_path.open(encoding='utf8') as deck_file:
            return json.load(deck_file)

    @staticmethod
    def read_import_config(directory_path):
        file_path = directory_path.joinpath(IMPORT_CONFIG_NAME).with_suffix(CONFIG_EXTENSION)

        if not file_path.exists():
            return {}

        with file_path.open(encoding='utf8') as meta_file:
            return yaml.full_load(meta_file)

    @staticmethod
    def import_deck_from_path(collection, directory_path):
        importer = AnkiJsonImporter(collection)
        try:
            deck_json, import_config = importer.load_deck_with_settings(directory_path)

            if deck_json is not None:
                importer.load_deck(deck_json, directory_path, import_config=import_config)
                aqt.utils.showInfo("Import of {} deck was successful".format(directory_path.name))
        except ValueError as error:
            aqt.utils.showWarning("Error: {}. While trying to import deck from directory {}".format(
                error.args[0], directory_path))
            raise

    @staticmethod
    def import_deck(collection, directory_provider: Callable[[str], Optional[str]]):
        directory_path = str(directory_provider("Select Deck Directory"))
        if directory_path:
            AnkiJsonImporter.import_deck_from_path(collection, Path(directory_path))
