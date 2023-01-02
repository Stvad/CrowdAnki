import os

import anki.exporting
import anki.hooks
import anki.utils
import aqt.exporting # Old 2.1.54- exporter
try:
    import aqt.import_export.exporting # New 2.1.55+ exporter
    NEW_EXPORTER_AVAILABLE = True
except ModuleNotFoundError:
    NEW_EXPORTER_AVAILABLE = False
import aqt.utils
from aqt import QFileDialog
from aqt.exporting import ExportDialog
from ...utils import constants


# aqt part:


def exporter_changed(self, exporter_id):
    self.exporter = aqt.exporting.exporters(self.col)[exporter_id][1](self.col)
    self.frm.includeMedia.setVisible(hasattr(self.exporter, "includeMedia"))


def get_save_file(parent, title, dir_description, key, ext, fname=None):
    # Anki 2.1.55+ passes ".extension" here.  Earlier versions passed just "extension".
    if ext in [constants.ANKI_EXPORT_EXTENSION, "." + constants.ANKI_EXPORT_EXTENSION]:
        directory = str(QFileDialog.getExistingDirectory(caption="Select Export Directory",
                                                         directory=fname))
        if directory:
            return os.path.join(directory, str(anki.utils.int_time()))
        return None

    return aqt.utils.getSaveFile_old(parent, title, dir_description, key, ext, fname)


ExportDialog.exporterChanged = anki.hooks.wrap(ExportDialog.exporterChanged, exporter_changed)

aqt.utils.getSaveFile_old = aqt.utils.getSaveFile

# Overriding instance imported with from style import
aqt.exporting.getSaveFile = get_save_file # Anki 2.1.54-
if NEW_EXPORTER_AVAILABLE:
    aqt.import_export.exporting.getSaveFile = get_save_file # Anki 2.1.55+

aqt.utils.getSaveFile = get_save_file
