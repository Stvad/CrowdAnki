from collections import namedtuple
from dataclasses import dataclass
from enum import Enum

from aqt.qt import *
from typing import List, Tuple

from .import_ui import Ui_Dialog as ConfigUI
from ..config.config_settings import ConfigSettings

from ..utils.utils import string_cs_to_list

ConfigEntry = namedtuple("ConfigEntry", ["config_name", "default_value"])


class ImportJsonSetting:
    import_message: str
    suggest_tag_imported_cards: bool
    personal_fields: List[Tuple[str, str]] = []

    class Properties(Enum):
        IMPORT_MESSAGE = ConfigEntry("import_message", "")
        SUGGEST_TAG_IMPORTED_CARDS = ConfigEntry("suggest_tag_imported_cards", False)

    def __init__(self, settings_dict: dict):
        for prop in self.Properties:
            setattr(self, prop.value.config_name, settings_dict.get(prop.value.config_name, prop.value.default_value))

        models = settings_dict.get("note_models", [])
        for model_name in models:
            personal_fields = models[model_name].get("personal_fields", [])
            for pf in personal_fields:
                self.personal_fields.append((model_name, pf))


class ImportConfig:
    personal_fields: List[Tuple[str, str]] = []
    add_tag_to_cards: List[str] = []

    use_header: bool = True
    use_note_models: bool = True
    use_notes: bool = True
    use_media: bool = True

    ignore_deck_movement: bool = False

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
        self.import_settings = ImportJsonSetting(config)
        self.ui_initial_setup()

        self.final_import_config: ImportConfig = None

    def accept(self):
        self.get_import_config()
        super().accept()

    def reject(self):
        self.get_import_config()
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
            add_header(model_name)

            for field in model["flds"]:
                field_name = field["name"]
                add_field(field_name, (model_name, field_name) in self.import_settings.personal_fields)

    def setup_misc(self):
        self.form.import_message_textbox.setText(self.import_settings.import_message)

        if self.import_settings.suggest_tag_imported_cards:
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

        # TODO: Deck Parts to Use

    def get_import_config(self):
        config = ImportConfig()

        config.personal_fields = []
        current_note_model = ""
        fields: List[QListWidgetItem] = [self.form.list_personal_fields.item(i) for i in
                                         range(self.form.list_personal_fields.count())]
        for field in fields:
            if not field.flags() & Qt.ItemIsUserCheckable:  # Note Model Header
                current_note_model = field.text()
            elif field.checkState() == Qt.Checked:  # Field
                config.personal_fields.append((current_note_model, field.text()))

        config.add_tag_to_cards = string_cs_to_list(
            self.form.textedit_tags.text()) if self.form.cb_tag_cards.isChecked() else []

        config.use_header = self.form.cb_headers.isChecked()
        config.use_note_models = self.form.cb_note_models.isChecked()
        config.use_notes = self.form.cb_notes.isChecked()
        config.use_media = self.form.cb_media.isChecked()

        config.ignore_deck_movement = self.form.cb_ignore_move_cards.isChecked()

        self.final_import_config = config
