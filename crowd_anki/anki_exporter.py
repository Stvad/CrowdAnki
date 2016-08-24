import json
import os
import shutil
from pathlib2 import Path

from crowd_anki.utils.constants import DECK_FILE_EXTENSION, MEDIA_SUBDIRECTORY_NAME
from crowd_anki.representation.deck import Deck


class AnkiJsonExporter(object):
    def __init__(self, collection):
        self.collection = collection

    def export_deck_to_directory(self, deck_name, output_dir=Path("."), copy_media=True):
        deck_directory = output_dir.joinpath(deck_name)

        deck_directory.mkdir(parents=True, exist_ok=True)

        deck = Deck.from_collection(self.collection, deck_name)
        deck_filename = deck_directory.joinpath(deck_name).with_suffix(DECK_FILE_EXTENSION)
        with deck_filename.open(mode='w') as deck_file:
            deck_file.write(unicode(json.dumps(deck,
                                               default=Deck.default_json,
                                               sort_keys=True,
                                               indent=4,
                                               ensure_ascii=False)))

        self._save_changes()

        if copy_media:
            self._copy_media(deck, deck_directory)

    def _save_changes(self):
        """Save updates that were maid during the export. E.g. UUID fields"""
        # This saves decks and deck configurations
        self.collection.decks.save()
        self.collection.decks.flush()

        self.collection.models.save()
        self.collection.models.flush()

        # Notes?

    def _copy_media(self, deck, deck_directory):
        media_directory = deck_directory.joinpath(MEDIA_SUBDIRECTORY_NAME)

        media_directory.mkdir(parents=True, exist_ok=True)

        for file_src in deck.get_media_file_list():
            shutil.copy(os.path.join(self.collection.media.dir(), file_src),
                        str(media_directory.resolve()))
