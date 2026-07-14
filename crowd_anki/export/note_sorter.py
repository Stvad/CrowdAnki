from ..config.config_settings import ConfigSettings, NoteSortingMethods
from ..representation.deck import Deck

import re

class NoteSorter:
    sorting_definitions = {
        # NO_SORTING is a special case which should be ignored by should_sort
        # However it's been kept here for edge cases, and for ease of testing
        # It returns 1 to ensure stable sorting, so the results will be in their previous order
        NoteSortingMethods.NO_SORTING: lambda i: 1,

        NoteSortingMethods.GUID: lambda i: i.anki_object.guid,
        NoteSortingMethods.FLAG: lambda i: i.anki_object.flags,
        NoteSortingMethods.TAG: lambda i: i.anki_object.tags,
        NoteSortingMethods.TAG_N: lambda i: NoteSorter.numeric_list(i.anki_object.tags),
        NoteSortingMethods.NOTE_ID: lambda i: i.anki_object.id,
        NoteSortingMethods.NOTE_MODEL_NAME: lambda i: i.anki_object._model["name"],
        NoteSortingMethods.NOTE_MODEL_ID: lambda i: i.anki_object._model["crowdanki_uuid"],
        NoteSortingMethods.FIELD1: lambda i: i.anki_object.fields[0],
        NoteSortingMethods.FIELD1_N: lambda i: NoteSorter.numeric_list(i.anki_object.fields[0]),
        NoteSortingMethods.FIELD2: lambda i: i.anki_object.fields[1],
        NoteSortingMethods.FIELD_LAST: lambda i: i.anki_object.fields[-1],
        NoteSortingMethods.BROWSER_SORT_FIELD: lambda i: i.anki_object.fields[i.anki_object._model['sortf']]
    }
    
    def __init__(self, config: ConfigSettings):
        self.sort_methods = config.formatted_export_note_sort_methods
        self.is_reversed = config.export_notes_reverse_order

    def should_sort(self):
        return self.sort_methods[0] != NoteSortingMethods.NO_SORTING

    def sort_notes(self, notes):
        if self.should_sort():
            notes = sorted(notes, key=self.get_sort_key)

        if self.is_reversed:
            notes = list(reversed(notes))

        return notes

    def sort_deck(self, deck: Deck):
        """Sort deck and its subdecks recursively."""
        deck.notes = self.sort_notes(deck.notes)

        for child_deck in deck.children:
            self.sort_deck(child_deck)

    def get_sort_key(self, note):   
        return tuple(
            key(note) 
            for key in tuple(
                self.sorting_definitions[method_name]
                for method_name in self.sort_methods
            )
        )

    # premature optimisation?
    numeric_list_regex = re.compile(r'^([^0-9]*)([0-9]*)(.*)$')

    @staticmethod
    def numeric_list(s):
        """Split string into a list of alternating strings and integers.

        The listed strings do not contain any numeric characters.  The
        integers are non-negative.

        For example, 'section1.42' will return ['section', 1, '.', 42].

        This function is used to allow sorting strings containing numerals
        more "naturally".

        """
        m = NoteSorter.numeric_list_regex.match(s)
        (prefix, integer, suffix) = m.groups()
        if integer:
            l = [prefix, int(integer)]
            if suffix:
                return l + NoteSorter.numeric_list(suffix)
            else:
                return l
        else:
            return [prefix]
