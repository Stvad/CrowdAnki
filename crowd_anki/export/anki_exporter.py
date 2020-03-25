import json
import os

import shutil
from pathlib import Path
from typing import Callable


from .deck_exporter import DeckExporter
from ..anki.adapters.anki_deck import AnkiDeck
from ..representation import deck_initializer
from ..representation.deck import Deck
from ..utils.constants import DECK_FILE_NAME, DECK_FILE_EXTENSION, MEDIA_SUBDIRECTORY_NAME
from ..utils.filesystem.name_sanitizer import sanitize_anki_deck_name
from .note_sorter import NoteSorter
from ..config.config_settings import ConfigSettings


class AnkiJsonExporter(DeckExporter):
    def __init__(self, collection,
                 config: ConfigSettings,
                 deck_name_sanitizer: Callable[[str], str] = sanitize_anki_deck_name,
                 deck_file_name: str = DECK_FILE_NAME):
        self.config = config
        self.collection = collection
        self.last_exported_count = 0
        self.deck_name_sanitizer = deck_name_sanitizer
        self.deck_file_name = deck_file_name
        self.note_sorter = NoteSorter(config)
    
    def export_to_directory(self, deck: AnkiDeck, output_dir=Path("."), copy_media=True, create_directory=True) -> Path:
        deck_directory = output_dir
        if create_directory:
            deck_directory = output_dir.joinpath(self.deck_name_sanitizer(deck.name))
            deck_directory.mkdir(parents=True, exist_ok=True)

        deck = deck_initializer.from_collection(self.collection, deck.name)

        deck.notes = self.note_sorter.sort_notes(deck.notes)

        self.last_exported_count = deck.get_note_count()

        deck_filename = deck_directory.joinpath(self.deck_file_name).with_suffix(DECK_FILE_EXTENSION)
        with deck_filename.open(mode='w', encoding="utf8") as deck_file:
            deck_file.write(json.dumps(deck,
                                       default=Deck.default_json,
                                       sort_keys=True,
                                       indent=4,
                                       ensure_ascii=False))

        self._save_changes()

        if copy_media:
            self._copy_media(deck, deck_directory)

        return deck_directory

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
            try:
                shutil.copy(os.path.join(self.collection.media.dir(), file_src),
                            str(media_directory.resolve()))
            except IOError as ioerror:
                print("Failed to copy a file {}. Full error: {}".format(file_src, ioerror))