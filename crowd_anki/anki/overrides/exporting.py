import os

import anki.exporting
import anki.hooks
import anki.utils
import aqt.exporting
import aqt.utils
from aqt import QFileDialog
from aqt.exporting import ExportDialog
from ...utils import constants


# aqt part:


def exporter_changed(self, exporter_id):
    self.exporter = aqt.exporting.exporters(self.col)[exporter_id][1](self.col)
    self.frm.includeMedia.setVisible(hasattr(self.exporter, "includeMedia"))


def get_save_file(parent, title, dir_description, key, ext, fname=None):
    if ext == constants.ANKI_EXPORT_EXTENSION:
        directory = str(QFileDialog.getExistingDirectory(caption="Select Export Directory",
                                                         directory=fname))
        if directory:
            return os.path.join(directory, str(anki.utils.int_time()))
        return None

    return aqt.utils.getSaveFile_old(parent, title, dir_description, key, ext, fname)


ExportDialog.exporterChanged = anki.hooks.wrap(ExportDialog.exporterChanged, exporter_changed)

aqt.utils.getSaveFile_old = aqt.utils.getSaveFile
aqt.exporting.getSaveFile = get_save_file  # Overriding instance imported with from style import
aqt.utils.getSaveFile = get_save_file
