from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import List

from aqt.qt import QDialog, QListWidgetItem, Qt, QFont, QSize

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
    personal_fields: defaultdict = field(init=False, default_factory=lambda: defaultdict(list))

    def is_personal_field(self, model_name, field_name):
        if model_name in self.personal_fields:
            if field_name in self.personal_fields[model_name]:
                return True
        return False

    def add_field(self, model_name, field_name):
        self.personal_fields[model_name].append(field_name)


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
            setattr(new_cls, prop.value.config_name,
                    settings_dict.get(prop.value.config_name, prop.value.default_value))
        new_cls._setup_personal_fields(settings_dict)
        return new_cls

    def _setup_personal_fields(self, settings_dict):
        models = settings_dict.get("note_models", dict())
        for model_name, keys in models.items():
            self.personal_fields.setdefault(model_name, keys.get("personal_fields", []))


@dataclass
class ImportConfig(PersonalFieldsHolder):
    add_tag_to_cards: List[str]

    use_notes: bool
    use_media: bool

    ignore_deck_movement: bool


class ImportDialog(QDialog):
    def __init__(self, deck_json, config, parent=None):
        super().__init__(None)
        self.parent = parent
        self.form = ConfigUI()
        self.form.setupUi(self)
        self.userConfig = ConfigSettings.get_instance()
        self.deck_json = deck_json
        self.import_defaults = ImportDefaults.from_dict(config)
        self.personal_field_ui_dict = defaultdict(dict)
        self.ui_initial_setup()

        self.final_import_config: ImportConfig = None

    def accept(self):
        self.read_import_config()
        super().accept()

    def ui_initial_setup(self):
        self.setup_personal_field_selection()
        self.setup_misc()
        self.setup_deck_part_checkboxes()

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

        def add_field(name, is_personal) -> QListWidgetItem:
            field_ui = QListWidgetItem(name)
            field_ui.setCheckState(Qt.Checked if is_personal else Qt.Unchecked)
            field_ui.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
            self.form.list_personal_fields.addItem(field_ui)
            return field_ui

        for model in self.deck_json["note_models"]:
            model_name = model["name"]
            model_id = model[UUID_FIELD_NAME]
            add_header(model_name)

            for field in model["flds"]:
                field_name = field["name"]
                field_ui = add_field(field_name, self.import_defaults.is_personal_field(model_name, field_name))
                self.personal_field_ui_dict[model_name].setdefault(field_name, field_ui)

    def setup_misc(self):
        self.form.import_message_textbox.setText(self.import_defaults.import_message)

        if self.import_defaults.suggest_tag_imported_cards:
            self.form.cb_tag_cards.setCheckState(Qt.Checked)
            self.form.cb_tag_cards.setText("Tag Cards (Suggested by Deck Maintainer!)")
        # else:
        # set as default from config settings

        if self.userConfig.import_notes_ignore_deck_movement:
            self.form.cb_ignore_move_cards.setCheckState(Qt.Checked)

    def setup_deck_part_checkboxes(self):
        def set_checked_and_text(checkbox, text, count, checked: bool = True):
            checkbox.setCheckState(Qt.Checked if checked else Qt.Unchecked)
            if count is not None:
                text = f"{text}: {'{:,}'.format(count)}"
            checkbox.setText(text)

        set_checked_and_text(self.form.cb_notes, "Notes", len(self.deck_json['notes']))
        set_checked_and_text(self.form.cb_media, "Media Files", len(self.deck_json['media_files']))

        # TODO: Deck Parts to Use, check which are actually in the deck_json

    def read_import_config(self):
        config = ImportConfig(
            add_tag_to_cards=string_cs_to_list(
                self.form.textedit_tags.text()) if self.form.cb_tag_cards.isChecked() else [],

            use_notes=self.form.cb_notes.isChecked(),
            use_media=self.form.cb_media.isChecked(),

            ignore_deck_movement=self.form.cb_ignore_move_cards.isChecked()
        )

        self.read_personal_fields(config)

        self.final_import_config = config

    def read_personal_fields(self, config):
        for model_name, fields_dict in self.personal_field_ui_dict.items():
            for field_name, widget_item in fields_dict.items():
                if widget_item.checkState() == Qt.Checked:
                    config.add_field(model_name, field_name)
