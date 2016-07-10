import json
import shutil
from pathlib import Path

from crowd_anki.utils.constants import DECK_FILE_EXTENSION, MEDIA_SUBDIRECTORY_NAME
from representation.deck import Deck


class AnkiJsonImporter(object):
    def __init__(self, collection):
        self.collection = collection

    def load_from_file(self, file_path):
        """
        Load deck from json file
        :type file_path: Path
        """
        deck = None
        with file_path.open() as deck_file:
            deck_json = json.load(deck_file)
            deck = Deck.from_json(deck_json)
            deck.save_to_collection(self.collection)

    def load_from_directory(self, directory_path, import_media=True):
        """
        Load deck serialized to directory
        Assumes that deck json file is located in the directory and named
        same way as a directory but with json file extension.
        :param import_media: Should we copy media?
        :type directory_path: Path
        """
        self.load_from_file(directory_path.joinpath(directory_path.name).with_suffix(DECK_FILE_EXTENSION))

        if not import_media:
            return

        for filename in directory_path.joinpath(MEDIA_SUBDIRECTORY_NAME).iterdir():
            shutil.copy(str(filename.resolve()), self.collection.media.dir())
