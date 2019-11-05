from collections import namedtuple
from enum import Enum

from aqt import mw
from ..utils.constants import USER_FILES_PATH

ConfigEntry = namedtuple("ConfigEntry", ["config_name", "default_value"])


class NoteSortingMethods(Enum):
    FIELD1 = "field1"
    FIELD2 = "field2"
    NO_SORTING = "none"
    GUID = "guid"
    FLAG = "flag"
    TAG = "tag"
    NOTE_MODEL = "notemodel"
    NOTE_MODEL_ID = "notemodelid"

    @classmethod
    def values(cls):
        return set(it.value for it in cls)


class ConfigSettings:
    snapshot_path: str
    automated_snapshot: bool
    snapshot_root_decks: list
    export_notes_reverse_order: bool
    export_note_sort_methods: list

    @property
    def formatted_export_note_sort_methods(self) -> list:
        return [
            NoteSortingMethods(method)
            for method in self.export_note_sort_methods
        ]

    class Properties(Enum):
        SNAPSHOT_PATH = ConfigEntry("snapshot_path", str(USER_FILES_PATH.resolve()))
        AUTOMATED_SNAPSHOT = ConfigEntry("automated_snapshot", False)
        SNAPSHOT_ROOT_DECKS = ConfigEntry("snapshot_root_decks", [])
        EXPORT_NOTE_SORT_METHODS = ConfigEntry("export_note_sort_methods", [NoteSortingMethods.NO_SORTING.value])
        EXPORT_NOTES_REVERSE_ORDER = ConfigEntry("export_notes_reverse_order", False)

    def __init__(self):
        self._config = mw.addonManager.getConfig(__name__)
        self.load_values()

    def _get(self, prop: Properties):
        return self._config.get(prop.value.config_name, prop.value.default_value)

    def load_values(self):
        for prop in self.Properties:
            setattr(self, prop.value.config_name, self._get(prop))

    def save(self):
        for prop in self.Properties:
            self._config[prop.value.config_name] = getattr(self, prop.value.config_name)

        mw.addonManager.writeConfig(__name__, self._config)

    def find_invalid_config_values(self):
        self.handle_empty_textboxes()

        incorrect_sort_methods = [method
                                  for method in self.export_note_sort_methods
                                  if method not in NoteSortingMethods.values()]

        return incorrect_sort_methods

    def handle_empty_textboxes(self):
        if not self.export_note_sort_methods[0]:
            self.set_property_to_default_value(self.Properties.EXPORT_NOTE_SORT_METHODS)

        if not self.snapshot_path:
            self.set_property_to_default_value(self.Properties.SNAPSHOT_PATH)

    def set_property_to_default_value(self, prop):
        setattr(self, prop.value.config_name, prop.value.default_value)
