"""
Config dialog entry point.
This module will load the config initially.
Write actions will be triggered here when the user clicks the dialog "Save All" button.
"""

from aqt.qt import *

from .config_ui import Ui_Dialog as ConfigUI
from .config_properties import ConfigValues, DeckExportSortMethods


class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.config = ConfigValues()
        self.form = ConfigUI()
        self.form.setupUi(self)
        self.ui_initial_setup()

    def accept(self):
        self.config.set_all_values()
        self.config.write_values_to_anki()
        super().accept()

    def reject(self):
        print("Reject")
        super().reject()

    def ui_initial_setup(self):
        self.form.cb_automated_snapshot.setChecked(self.config.automated_snapshot)
        self.form.cb_automated_snapshot.stateChanged.connect(self.toggle_automated_snapshot)

        self.form.textedit_snapshot_root_decks.appendPlainText(self.config.get_formatted_sort_methods())

        self.form.cb_reverse_sort.setChecked(self.config.export_deck_sort_reversed)
        self.form.cb_reverse_sort.stateChanged.connect(self.toggle_reverse_sort)
    

    def toggle_automated_snapshot(self):
        self.config.automated_snapshot = not self.config.automated_snapshot

    def toggle_reverse_sort(self):
        self.config.export_deck_sort_reversed = not self.config.export_deck_sort_reversed
    
    