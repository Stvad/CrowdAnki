import json
import os

import shutil
from pathlib import Path
from typing import Callable
import re

from .deck_exporter import DeckExporter
from ..anki.adapters.anki_deck import AnkiDeck
from ..representation import deck_initializer
from ..representation.deck import Deck
from ..utils.constants import DECK_FILE_NAME, DECK_FILE_EXTENSION, MEDIA_SUBDIRECTORY_NAME
from ..utils.filesystem.name_sanitizer import sanitize_anki_deck_name
from ..utils.config import EXPORT_DECK_SORT


class AnkiJsonExporter(DeckExporter):
    def __init__(self, collection, config,
                 deck_name_sanitizer: Callable[[str], str] = sanitize_anki_deck_name,
                 deck_file_name: str = DECK_FILE_NAME):
        self.config = config
        self.collection = collection
        self.last_exported_count = 0
        self.deck_name_sanitizer = deck_name_sanitizer
        self.deck_file_name = deck_file_name        
    
    def export_to_directory(self, deck: AnkiDeck, output_dir=Path("."), copy_media=True) -> Path:
        deck_directory = output_dir.joinpath(self.deck_name_sanitizer(deck.name))

        deck_directory.mkdir(parents=True, exist_ok=True)

        deck = deck_initializer.from_collection(self.collection, deck.name)
        deck.notes = self.sort_notes(deck.notes)
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

    def sort_notes(self, notes):
        deck_sort_config = self.config.get(EXPORT_DECK_SORT, False)

        if not deck_sort_config or "method" not in deck_sort_config:
            return notes

        sort_method = deck_sort_config["method"]
        is_reversed = deck_sort_config["reversed"] if "reversed" in deck_sort_config else False

        def _formatted_sort_method(method):
            return re.sub("[-_\s+]", "", method).lower()

        # Make sure formatting of sort_method is correct, and format each entry
        if isinstance(sort_method, str):
            sort_method = [_formatted_sort_method(sort_method)]
        elif isinstance(sort_method, list):
            if len(sort_method) == 1:
                sort_method = [_formatted_sort_method(sort_method[0])]
            elif len(sort_method) > 1:
                sort_method = [_formatted_sort_method(sm) for sm in sort_method]                
            else:
                return notes
        else:
            return notes

        # Create mapping of sortable_values variable, to sort_method keys, to sortable_values lambda
        sorting_definitions = [
            (0, ("guid", "guids"), lambda i: i.anki_object.guid),
            (1, ("flag", "flags"), lambda i: i.anki_object.flags),
            (2, ("tag", "tags"), lambda i: i.anki_object.tags),
            (3, ("notemodel", "notemodels", "notemodelname", "notemodelsname", "notemodelnames", "notemodelsnames"), lambda i: i.anki_object._model["name"]),
            (4, ("notemodelid", "notemodelsid", "notemodelids", "notemodelsids"), lambda i: i.anki_object._model["crowdanki_uuid"]),
            (5, ("field1", "firstfield", "first"), lambda i: i.anki_object.fields[0]),
            (6, ("field2", "secondfield", "second"), lambda i: i.anki_object.fields[1])
        ]

        # Extract each notes values which could be used for sorting into sortable_values, for use later on
        for note in notes:
            note.sortable_values = [None] * len(sorting_definitions)
            note.export_filter_set.add("sortable_values")

            for defs in sorting_definitions:
                note.sortable_values[defs[0]] = defs[2](note)


        # Flatten out the sorting_definitions to a map with one value per entry
        sort_map = {singlekey:num for num, keytuple, lam in sorting_definitions for singlekey in keytuple}


        if sort_method[0] in ["default", "none", "nosorting"]:      # Only the first method is considered for these pass variables
            if not is_reversed:
                pass
            else:
                notes = list(reversed(notes))
        else:
            all_methods_good = True
            for method in sort_method:
                if method not in sort_map:
                    all_methods_good = False
                    break
            
            # Only continue if all sorting methods are known
            if all_methods_good:
                sort_numbers = [sort_map[sm] for sm in sort_method]

                if len(sort_numbers) == 1:
                    sort_keys = lambda i: i.sortable_values[sort_numbers[0]]
                elif len(sort_numbers) == 2:
                    sort_keys = lambda i: (i.sortable_values[sort_numbers[0]], i.sortable_values[sort_numbers[1]])
                elif len(sort_numbers) == 3:
                    sort_keys = lambda i: (i.sortable_values[sort_numbers[0]], i.sortable_values[sort_numbers[1]], i.sortable_values[sort_numbers[2]])
                elif len(sort_numbers) >= 4:    ### Anything more than 4 is ignored
                    sort_keys = lambda i: (i.sortable_values[sort_numbers[0]], i.sortable_values[sort_numbers[1]], i.sortable_values[sort_numbers[2]], i.sortable_values[sort_numbers[3]])

                notes = sorted(notes, key=sort_keys, reverse=is_reversed)

        return notes