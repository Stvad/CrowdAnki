"""
Config dialog entry point.
This module will load the config initially.
Write actions will be triggered here when the user clicks the dialog "Save All" button.
"""

from aqt.qt import *

from .config_ui import Ui_Dialog as ConfigUI
from .config_settings import ConfigSettings

from PyQt5 import QtCore, QtGui, QtWidgets

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.config = ConfigSettings()
        self.form = ConfigUI()
        self.form.setupUi(self)
        self.ui_initial_setup()

    def accept(self):
        invalid_values = self.config.find_invalid_config_values()
        if invalid_values:
            print(invalid_values)
            self.error_message_popup = QMessageBox(self)
            message_text = "\" , \"".join(invalid_values)
            self.error_message_popup.setText(f"Invalid config values: \"{message_text}\"")
            self.error_message_popup.open()
        else:
            self.config.set_all_values()
            self.config.write_values_to_anki()
            super().accept()

    def reject(self):
        print("Reject")
        super().reject()

    def ui_initial_setup(self):
        self.form.textedit_snapshot_path.setText(self.config.snapshot_path)
        self.form.textedit_snapshot_path.textChanged.connect(self.changed_textedit_snapshot_path)

        self.form.cb_automated_snapshot.setChecked(self.config.automated_snapshot)
        self.form.cb_automated_snapshot.stateChanged.connect(self.toggle_automated_snapshot)

        self.form.textedit_snapshot_root_decks.appendPlainText(self.get_formatted_comma_separated_string(self.config.snapshot_root_decks))
        self.form.textedit_snapshot_root_decks.textChanged.connect(self.changed_textedit_snapshot_root_decks)

        self.form.cb_reverse_sort.setChecked(self.config.export_deck_sort_reversed)
        self.form.cb_reverse_sort.stateChanged.connect(self.toggle_reverse_sort)
    
        self.form.textedit_deck_sort_methods.appendPlainText(self.get_formatted_comma_separated_string(self.config.export_deck_sort_methods))
        self.form.textedit_deck_sort_methods.textChanged.connect(self.changed_textedit_deck_sort_methods)

    def toggle_automated_snapshot(self):
        self.config.automated_snapshot = not self.config.automated_snapshot

    def toggle_reverse_sort(self):
        self.config.export_deck_sort_reversed = not self.config.export_deck_sort_reversed
    
    def changed_textedit_deck_sort_methods(self):
        self.config.export_deck_sort_methods = self.get_unformatted_list(self.form.textedit_deck_sort_methods.toPlainText())
    
    def changed_textedit_snapshot_root_decks(self):
        self.config.snapshot_root_decks = self.get_unformatted_list(self.form.textedit_snapshot_root_decks.toPlainText())
    
    def changed_textedit_snapshot_path(self):
        self.config.snapshot_path = self.form.textedit_snapshot_path.text()

    def get_formatted_comma_separated_string(self, ufList: list) -> str:
        return ', '.join(ufList)
        
    def get_unformatted_list(self, fList: str) -> list:
        return [x.strip() for x in fList.split(',')]