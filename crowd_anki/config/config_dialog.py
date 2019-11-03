"""
Config dialog entry point.
This module will load the config initially.
Write actions will be triggered here when the user clicks the dialog "Save All" button.
"""

from aqt.qt import *

from .config_ui import Ui_Dialog as ConfigUI
from .config_settings import ConfigSettings


class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(None)
        self.parent = parent
        self.config = ConfigSettings()
        self.form = ConfigUI()
        self.form.setupUi(self)
        self.ui_initial_setup()

    def accept(self):
        invalid_values = self.config.find_invalid_config_values()
        if invalid_values:
            error_message_popup = QMessageBox(self)
            message_text = "\" , \"".join(invalid_values)
            error_message_popup.setText(f"Invalid config values: \"{message_text}\"")
            error_message_popup.open()
        else:
            self.config.save_values_to_anki()
            super().accept()

    def ui_initial_setup(self):
        self.form.textedit_snapshot_path.setText(self.config.snapshot_path)
        self.form.textedit_snapshot_path.textChanged.connect(self.changed_textedit_snapshot_path)

        self.form.cb_automated_snapshot.setChecked(self.config.automated_snapshot)
        self.form.cb_automated_snapshot.stateChanged.connect(self.toggle_automated_snapshot)

        self.form.textedit_snapshot_root_decks.appendPlainText(
            self.list_to_cs_string(self.config.snapshot_root_decks)
        )
        self.form.textedit_snapshot_root_decks.textChanged.connect(self.changed_textedit_snapshot_root_decks)

        self.form.cb_reverse_sort.setChecked(self.config.export_notes_reverse_order)
        self.form.cb_reverse_sort.stateChanged.connect(self.toggle_reverse_sort)

        self.form.textedit_deck_sort_methods.appendPlainText(
            self.list_to_cs_string(self.config.export_note_sort_methods)
        )
        self.form.textedit_deck_sort_methods.textChanged.connect(self.changed_textedit_deck_sort_methods)

    def toggle_automated_snapshot(self):
        self.config.automated_snapshot = not self.config.automated_snapshot

    def toggle_reverse_sort(self):
        self.config.export_notes_reverse_order = not self.config.export_notes_reverse_order

    def changed_textedit_deck_sort_methods(self):
        self.config.export_note_sort_methods = self.string_cs_to_list(
            self.form.textedit_deck_sort_methods.toPlainText()
        )

    def changed_textedit_snapshot_root_decks(self):
        self.config.snapshot_root_decks = self.string_cs_to_list(self.form.textedit_snapshot_root_decks.toPlainText())

    def changed_textedit_snapshot_path(self):
        self.config.snapshot_path = self.form.textedit_snapshot_path.text()

    @staticmethod
    def list_to_cs_string(uf_list: list) -> str:
        return ', '.join(uf_list)

    @staticmethod
    def string_cs_to_list(f_list: str) -> list:
        return [x.strip() for x in f_list.split(',')]
