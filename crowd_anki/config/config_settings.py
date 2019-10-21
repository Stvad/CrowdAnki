from enum import Enum
from dataclasses import dataclass

from aqt import mw
from ..utils.constants import USER_FILES_PATH

@dataclass
class ConfigSettings():
    class Properties(Enum):
        SNAPSHOT_PATH = "snapshot_path"
        AUTOMATED_SNAPSHOT = "automated_snapshot"
        SNAPSHOT_ROOT_DECKS = "snapshot_root_decks"
        EXPORT_DECK_SORT_METHODS = "export_deck_sort_method"
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

    snapshot_path: str
    automated_snapshot: bool
    snapshot_root_decks: list

    export_deck_sort_reversed: bool
    export_deck_sort_methods: list


    def __init__(self):
        self.config_file = mw.addonManager.getConfig(__name__)
        self.get_all_values()

    def get_all_values(self):
        self.snapshot_path = self.config_file.get(self.Properties.SNAPSHOT_PATH.value, str(USER_FILES_PATH.resolve()))
        self.automated_snapshot = self.config_file.get(self.Properties.AUTOMATED_SNAPSHOT.value, False)
        self.snapshot_root_decks = self.config_file.get(self.Properties.SNAPSHOT_ROOT_DECKS.value, [])

        self.export_deck_sort_reversed = self.config_file.get(self.Properties.EXPORT_DECK_SORT_REVERSED.value, False)
        self.export_deck_sort_methods = self.config_file.get(self.Properties.EXPORT_DECK_SORT_METHODS.value, [self.DeckExportSortMethods.NO_SORTING.value])


    def set_all_values(self):
        self.config_file.update({
            self.Properties.SNAPSHOT_PATH.value: self.snapshot_path,
            self.Properties.AUTOMATED_SNAPSHOT.value: self.automated_snapshot,
            self.Properties.EXPORT_DECK_SORT_REVERSED.value: self.export_deck_sort_reversed,

            self.Properties.SNAPSHOT_ROOT_DECKS.value: self.snapshot_root_decks,
            self.Properties.EXPORT_DECK_SORT_METHODS.value: self.export_deck_sort_methods
        })

    def write_values_to_anki(self):
        mw.addonManager.writeConfig(__name__, self.config_file)
    
    def find_invalid_config_values(self):
        self.handle_empty_textboxes()
        
        invalid_methods = [method for method in self.export_deck_sort_methods if method not in self.DeckExportSortMethods._value2member_map_]

        return invalid_methods
    
    def handle_empty_textboxes(self):
        if not self.export_deck_sort_methods:
            self.export_deck_sort_methods = [self.DeckExportSortMethods.NO_SORTING.value]
        
        if not self.snapshot_path:
            self.snapshot_path = str(USER_FILES_PATH.resolve())