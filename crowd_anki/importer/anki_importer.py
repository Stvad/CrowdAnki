import json
import os
import shutil
from pathlib import Path
from typing import Callable, Optional

import aqt
import aqt.utils

from ..representation import deck_initializer
from ..utils.constants import DECK_FILE_NAME, DECK_FILE_EXTENSION, MEDIA_SUBDIRECTORY_NAME


class AnkiJsonImporter:
    def __init__(self, collection, deck_file_name: str = DECK_FILE_NAME):
        self.collection = collection
        self.deck_file_name = deck_file_name

    def load_from_file(self, file_path):
        """
        Load deck from json file
        :type file_path: Path
        """
        if not file_path.exists():
            raise ValueError("There is no {} file inside of the selected directory".format(file_path))

        with file_path.open(encoding='utf8') as deck_file:
            deck_json = json.load(deck_file)
            deck = deck_initializer.from_json(deck_json)

            deck.save_to_collection(self.collection)

    def load_from_directory(self, directory_path, import_media=True):
        """
        Load deck serialized to directory
        Assumes that deck json file is located in the directory
        and named 'deck.json'
        :param import_media: Should we copy media?
        :type directory_path: Path
        """
        if aqt.mw:
            aqt.mw.backup()

        try:
            self.load_from_file(self.get_deck_path(directory_path))

            if import_media:
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
        """

        def path_for_name(name):
            return directory_path.joinpath(name).with_suffix(DECK_FILE_EXTENSION)

        convention_path = path_for_name(self.deck_file_name)
        inferred_path = path_for_name(directory_path.name)
        return convention_path if convention_path.exists() else inferred_path

    @staticmethod
    def import_deck_from_path(collection, directory_path, import_media=True):
        importer = AnkiJsonImporter(collection)
        try:
            importer.load_from_directory(directory_path, import_media)
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
