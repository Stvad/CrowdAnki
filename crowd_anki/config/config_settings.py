from collections import namedtuple
from enum import Enum
from pathlib import Path
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
    NOTE_MODEL_NAME = "note_model_name"
    NOTE_MODEL_ID = "note_model_id"

    @classmethod
    def values(cls):
        return set(it.value for it in cls)


class ConfigSettings:
    __instance = None

    snapshot_path: str
    automated_snapshot: bool
    snapshot_root_decks: list
    export_notes_reverse_order: bool
    export_note_sort_methods: list
    export_create_deck_subdirectory: bool
    import_notes_ignore_deck_movement: bool

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
        EXPORT_CREATE_DECK_SUBDIRECTORY = ConfigEntry("export_create_deck_subdirectory", True)
        IMPORT_NOTES_IGNORE_DECK_MOVEMENT = ConfigEntry("import_notes_ignore_deck_movement", False)

    def __init__(self, addon_manager=None, init_values=None, profile_manager=None):
        self._profile_manager = profile_manager or mw.pm
        self.addon_manager = addon_manager or mw.addonManager
        self._config = init_values or addon_manager.getConfig(__name__)
        self.load_values()

    @classmethod
    def get_instance(cls, addon_manager=None, profile_manager=None):
        if cls.__instance is None:
            cls.__instance = ConfigSettings(addon_manager=addon_manager, profile_manager=profile_manager)
        return cls.__instance

    @property
    def profileName(self):
        return self._profile_manager.name if self._profile_manager else ""

    @property
    def full_snapshot_path(self):
        return Path(self.snapshot_path).joinpath(self.profileName)

    def _get(self, prop: Properties):
        return self._config.get(prop.value.config_name, prop.value.default_value)

    def load_values(self):
        for prop in self.Properties:
            setattr(self, prop.value.config_name, self._get(prop))

    def save(self):
        for prop in self.Properties:
            self._config[prop.value.config_name] = getattr(self, prop.value.config_name)

        self.addon_manager.writeConfig(__name__, self._config)

    def find_invalid_config_values(self):
        self.try_infer_values()

        incorrect_sort_methods = [method
                                  for method in self.export_note_sort_methods
                                  if method not in NoteSortingMethods.values()]

        return incorrect_sort_methods

    def try_infer_values(self):
        if not self.export_note_sort_methods[0]:
            self.set_property_to_default_value(self.Properties.EXPORT_NOTE_SORT_METHODS)

        if not self.snapshot_path:
            self.set_property_to_default_value(self.Properties.SNAPSHOT_PATH)

    def set_property_to_default_value(self, prop):
        setattr(self, prop.value.config_name, prop.value.default_value)
