from collections import namedtuple
from dataclasses import dataclass, field
from enum import Enum

from aqt.qt import *
from typing import List, Tuple, Dict

from .import_ui import Ui_Dialog as ConfigUI
from ..config.config_settings import ConfigSettings
from ..utils.constants import UUID_FIELD_NAME

from ..utils.utils import string_cs_to_list


@dataclass
class ConfigEntry:
    config_name: str
    default_value: any


@dataclass
class PersonalFieldsHolder:
    personal_fields: Dict[str, List[str]] = field(init=False, default_factory=lambda: dict())

    def has_pf(self, field_name, *keys):
        def _check_pfs(key):
            if key in self.personal_fields:
                if field_name in self.personal_fields[key]:
                    return True
            return False
        return any(_check_pfs(key) for key in keys)

    def add_field(self, model_name, model_id, field_name):
        def _add(key):
            if key not in self.personal_fields:
                self.personal_fields.setdefault(key, [field_name])
            else:
                self.personal_fields[key].append(field_name)
        _add(model_id)
        _add(model_name)


@dataclass
class ImportDefaults(PersonalFieldsHolder):
    import_message: str = field(init=False)
    suggest_tag_imported_cards: bool = field(init=False)

    class Properties(Enum):
        IMPORT_MESSAGE = ConfigEntry("import_message", "")
        SUGGEST_TAG_IMPORTED_CARDS = ConfigEntry("suggest_tag_imported_cards", False)

    @classmethod
    def from_dict(cls, settings_dict: dict) -> 'ImportDefaults':
        new_cls = cls()
        for prop in cls.Properties:
            setattr(new_cls, prop.value.config_name, settings_dict.get(prop.value.config_name, prop.value.default_value))
        new_cls._setup_personal_fields(settings_dict)
        return new_cls

    def _setup_personal_fields(self, settings_dict):
        models = settings_dict.get("note_models", [])
        for model_name_or_id in models:
            self.personal_fields.setdefault(model_name_or_id, models[model_name_or_id].get("personal_fields", []))


@dataclass
class ImportConfig(PersonalFieldsHolder):
    add_tag_to_cards: List[str]

    use_header: bool
    use_note_models: bool
    use_notes: bool
    use_media: bool

    ignore_deck_movement: bool

    def __repr__(self):
        return f"ImportConfig({self.personal_fields!r}, {self.add_tag_to_cards!r}, " \
               f"{self.use_header!r}, {self.use_notes!r}, {self.use_note_models!r}, {self.use_media!r} " \
               f"{self.ignore_deck_movement!r})"


class ImportDialog(QDialog):
    def __init__(self, deck_json, config, parent=None):
        super().__init__(None)
        self.parent = parent
        self.form = ConfigUI()
        self.form.setupUi(self)
        self.userConfig = ConfigSettings.get_instance()
        self.deck_json = deck_json
        self.import_defaults = ImportDefaults.from_dict(config)
        self.ui_initial_setup()

        self.final_import_config: ImportConfig = None

    def accept(self):
        self.read_import_config()
        super().accept()

    def reject(self):
        super().reject()

    def ui_initial_setup(self):
        self.setup_personal_field_selection()
        self.setup_misc()

    def setup_personal_field_selection(self):
        heading_font = QFont()
        heading_font.setBold(True)
        heading_font.setUnderline(True)

        def add_header(name):
            heading_ui = QListWidgetItem(name)
            heading_ui.setFlags(Qt.ItemIsEnabled)
            heading_ui.setSizeHint(QSize(self.form.list_personal_fields.width(), 30))
            heading_ui.setFont(heading_font)
            self.form.list_personal_fields.addItem(heading_ui)

        def add_field(name, is_personal):
            field_ui = QListWidgetItem(name)
            field_ui.setCheckState(Qt.Checked if is_personal else Qt.Unchecked)
            field_ui.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
            self.form.list_personal_fields.addItem(field_ui)

        for model in self.deck_json["note_models"]:
            model_name = model["name"]
            model_id = model[UUID_FIELD_NAME]
            add_header(model_name)

            for field in model["flds"]:
                field_name = field["name"]
                add_field(field_name, self.import_defaults.has_pf(field_name, model_name, model_id))

    def setup_misc(self):
        self.form.import_message_textbox.setText(self.import_defaults.import_message)

        if self.import_defaults.suggest_tag_imported_cards:
            self.form.cb_tag_cards.setCheckState(Qt.Checked)
            self.form.cb_tag_cards.setText("Tag Cards (Suggested by Deck Manager!)")
        # else:
        # set as default from config settings

        if self.userConfig.import_notes_ignore_deck_movement:
            self.form.cb_ignore_move_cards.setCheckState(Qt.Checked)

        self.form.cb_headers.setCheckState(Qt.Checked)
        self.form.cb_note_models.setCheckState(Qt.Checked)
        self.form.cb_notes.setCheckState(Qt.Checked)
        self.form.cb_media.setCheckState(Qt.Checked)

        # TODO: Deck Parts to Use, check which are actually in the deck_json

    def read_import_config(self):
        config = ImportConfig(
            add_tag_to_cards=string_cs_to_list(
                self.form.textedit_tags.text()) if self.form.cb_tag_cards.isChecked() else [],

            use_header=self.form.cb_headers.isChecked(),
            use_note_models=self.form.cb_note_models.isChecked(),
            use_notes=self.form.cb_notes.isChecked(),
            use_media=self.form.cb_media.isChecked(),

            ignore_deck_movement=self.form.cb_ignore_move_cards.isChecked()
        )

        self.read_personal_fields(config)

        self.final_import_config = config

    def read_personal_fields(self, config):
        current_note_model = ""
        current_uuid = ""
        ui_fields: List[QListWidgetItem] = self.get_ui_pf_items()
        for ui_field in ui_fields:
            if not ui_field.flags() & Qt.ItemIsUserCheckable:  # Note Model Header
                current_note_model = ui_field.text()
                current_uuid = next(model[UUID_FIELD_NAME]
                                    for model in self.deck_json["note_models"] if model["name"] == current_note_model)
            elif ui_field.checkState() == Qt.Checked:  # Field
                config.add_field(current_note_model, current_uuid, ui_field.text())

    def get_ui_pf_items(self):
        return [self.form.list_personal_fields.item(i) for i in range(self.form.list_personal_fields.count())]
