from enum import Enum
from dataclasses import dataclass

from aqt import mw
from ..utils.constants import USER_FILES_PATH

@dataclass
class ConfigSettings:
    class Properties(Enum):
        SNAPSHOT_PATH = "snapshot_path"
        AUTOMATED_SNAPSHOT = "automated_snapshot"
        SNAPSHOT_ROOT_DECKS = "snapshot_root_decks"
        EXPORT_DECK_SORT_METHODS = "export_deck_sort_method"
        EXPORT_DECK_SORT_REVERSED = "export_deck_sort_reversed"


    class DeckExportSortMethods(Enum):
        FIELD1 = "field1"
        FIELD2 = "field2"
        NO_SORTING = "none"
        GUID = "guid"
        FLAG = "flag"
        TAG = "tag"
        NOTE_MODEL = "notemodel"
        NOTE_MODEL_ID = "notemodelid"

    snapshot_path: str
    automated_snapshot: bool
    snapshot_root_decks: list

    export_deck_sort_reversed: bool
    export_deck_sort_methods: list


    def __init__(self, get_settings = True):
        if get_settings:
            self._config = mw.addonManager.getConfig(__name__)
            self.get_all_values()

    def get_all_values(self):
        self.snapshot_path = self._config.get(self.Properties.SNAPSHOT_PATH.value, str(USER_FILES_PATH.resolve()))
        self.automated_snapshot = self._config.get(self.Properties.AUTOMATED_SNAPSHOT.value, False)
        self.snapshot_root_decks = self._config.get(self.Properties.SNAPSHOT_ROOT_DECKS.value, [])

        self.export_deck_sort_reversed = self._config.get(self.Properties.EXPORT_DECK_SORT_REVERSED.value, False)
        self.export_deck_sort_methods = self._config.get(self.Properties.EXPORT_DECK_SORT_METHODS.value, [self.DeckExportSortMethods.NO_SORTING.value])


    def save_values_to_anki(self):
        self._config.update({
            self.Properties.SNAPSHOT_PATH.value: self.snapshot_path,
            self.Properties.AUTOMATED_SNAPSHOT.value: self.automated_snapshot,
            self.Properties.EXPORT_DECK_SORT_REVERSED.value: self.export_deck_sort_reversed,

            self.Properties.SNAPSHOT_ROOT_DECKS.value: self.snapshot_root_decks,
            self.Properties.EXPORT_DECK_SORT_METHODS.value: self.export_deck_sort_methods
        })

        mw.addonManager.writeConfig(__name__, self._config)
    
    def find_invalid_config_values(self):
        self.handle_empty_textboxes()
        
        return [
            method for method in self.export_deck_sort_methods 
            if method not in self.DeckExportSortMethods._value2member_map_
        ]
    
    def handle_empty_textboxes(self):
        if not self.export_deck_sort_methods[0]:
            self.export_deck_sort_methods = [self.DeckExportSortMethods.NO_SORTING.value]
        
        if not self.snapshot_path:
            self.snapshot_path = str(USER_FILES_PATH.resolve())