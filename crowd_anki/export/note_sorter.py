import re
from dataclasses import dataclass

from ..config.config_settings import ConfigSettings

DEBUG = True

@dataclass
class NoteSorter():
    sort_method: list
    is_reversed: bool
    skip_sorting: bool
    sort_key_tuple: tuple

    @classmethod
    def from_config(cls, config: ConfigSettings):
        sorting_definitions = {
            ConfigSettings.DeckExportSortMethods.NO_SORTING: None,
            ConfigSettings.DeckExportSortMethods.GUID: lambda i: i.anki_object.guid,
            ConfigSettings.DeckExportSortMethods.FLAG: lambda i: i.anki_object.flags,
            ConfigSettings.DeckExportSortMethods.TAG: lambda i: i.anki_object.tags,
            ConfigSettings.DeckExportSortMethods.NOTEMODEL: lambda i: i.anki_object._model["name"],
            ConfigSettings.DeckExportSortMethods.NOTEMODELID: lambda i: i.anki_object._model["crowdanki_uuid"],
            ConfigSettings.DeckExportSortMethods.FIELD1: lambda i: i.anki_object.fields[0],
            ConfigSettings.DeckExportSortMethods.FIELD2: lambda i: i.anki_object.fields[1]
        }
        
        cls.sort_method = [ConfigSettings.DeckExportSortMethods._value2member_map_[method] for method in config.export_deck_sort_methods]
        cls.is_reversed = config.export_deck_sort_reversed

        cls.skip_sorting = True if cls.sort_method[0] == ConfigSettings.DeckExportSortMethods.NO_SORTING and not cls.is_reversed else False

        cls.sort_key_tuple = tuple(sorting_definitions[method_name] for method_name in cls.sort_method)

        return NoteSorter(
            sort_method=cls.sort_method,
            is_reversed=cls.is_reversed,
            skip_sorting=cls.skip_sorting,
            sort_key_tuple=cls.sort_key_tuple
        )

    def sort_notes(self, notes):
        if DEBUG:
            print([note.anki_object.guid for note in notes])

        if not self.skip_sorting:
            if self.sort_method[0] == ConfigSettings.DeckExportSortMethods.NO_SORTING:      # Only the first method is considered for these pass variables
                if not self.is_reversed:
                    pass
                else:
                    notes = list(reversed(notes))
            else:
                notes = sorted(notes, key=self.get_sort_key, reverse=self.is_reversed)

        if DEBUG:
            print([note.anki_object.guid for note in notes])

        return notes

    def get_sort_key(self, note):   
        return tuple(key(note) for key in self.sort_key_tuple)