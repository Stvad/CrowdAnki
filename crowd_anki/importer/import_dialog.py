
from aqt.qt import *

from .import_ui import Ui_Dialog as ConfigUI
# from .config_settings import ConfigSettings


class ImportDialog(QDialog):
    def __init__(self, config,
                 parent=None):
        super().__init__(None)
        self.parent = parent
        self.config = config
        self.form = ConfigUI()
        self.form.setupUi(self)
        self.ui_initial_setup()

    def accept(self):
        super().accept()

    def ui_initial_setup(self):
        self.setup_personal_fields()

    def setup_personal_fields(self):
        pfs = self.config["personal_fields"]
        self.form.list_personal_fields.addItems(pfs)
