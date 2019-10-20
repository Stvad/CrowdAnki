from enum import Enum
from dataclasses import dataclass

from aqt import mw


class ConfigProperties(Enum):
    AUTOMATED_SNAPSHOT = "automated_snapshot"
    SNAPSHOT_ROOT_DECKS = "snapshot_root_decks"
    EXPORT_DECK_SORT_METHOD = "export_deck_sort_method"
    EXPORT_DECK_SORT_REVERSED = "export_deck_sort_reversed"


class DeckExportSortMethods(Enum):
    NO_SORTING = "none"
    GUID = "guid"
    FLAG = "flag"
    TAG = "tag"
    NOTEMODEL = "notemodel"
    NOTEMODELID = "notemodelid"
    FIELD1 = "field1"
    FIELD2 = "field2"


@dataclass
class ConfigValues():
    automated_snapshot: bool
    snapshot_root_decks: list

    export_deck_sort_reversed: bool
    export_deck_sort_method: list


    def __init__(self):
        self.config_file = mw.addonManager.getConfig(__name__)
        self.get_all_values()

    def get_all_values(self):
        self.automated_snapshot = self.config_file.get(ConfigProperties.AUTOMATED_SNAPSHOT.value, False)
        self.snapshot_root_decks = self.config_file.get(ConfigProperties.SNAPSHOT_ROOT_DECKS.value, [])

        self.export_deck_sort_reversed = self.config_file.get(ConfigProperties.EXPORT_DECK_SORT_REVERSED.value, False)
        self.export_deck_sort_method = self.config_file.get(ConfigProperties.EXPORT_DECK_SORT_METHOD.value, [DeckExportSortMethods.NO_SORTING.value])


    def set_all_values(self):
        self.config_file.update({
            ConfigProperties.AUTOMATED_SNAPSHOT.value: self.automated_snapshot,
            ConfigProperties.SNAPSHOT_ROOT_DECKS.value: self.snapshot_root_decks,
            ConfigProperties.EXPORT_DECK_SORT_REVERSED.value: self.export_deck_sort_reversed,
            ConfigProperties.EXPORT_DECK_SORT_METHOD.value: self.export_deck_sort_method
        })

    def write_values_to_anki(self):
        mw.addonManager.writeConfig(__name__, self.config_file)
    
    def get_formatted_sort_methods(self):
        return ', '.join(self.export_deck_sort_method)
        
    def unformat_sort_methods(self):
        return [x.strip() for x in self.export_deck_sort_method.split(',')]