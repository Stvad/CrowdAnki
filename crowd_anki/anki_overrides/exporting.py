import os

import anki.hooks
import anki.utils
import aqt.utils
import aqt.exporting
from aqt import QFileDialog
import anki.exporting
from anki.exporting import AnkiExporter
from aqt.exporting import ExportDialog

from ..utils import constants


def get_files_for_models(self, model_ids, media_dir):
    result = set()
    for file_name in os.listdir(media_dir):
        if file_name.startswith("_"):
            # Scan all models in model_ids for reference to file_name
            for model in self.col.models.all():
                if int(model['id']) in model_ids:
                    if self._modelHasMedia(model, file_name):
                        result.add(file_name)
                        break
    return result


def get_exporter_id(exporter):
    return "{} (*{})".format(exporter.key, exporter.ext), exporter


AnkiExporter.get_files_for_models = get_files_for_models

# aqt part:


def exporter_changed(self, exporter_id):
    self.exporter = aqt.exporting.exporters()[exporter_id][1](self.col)
    self.frm.includeMedia.setVisible(hasattr(self.exporter, "includeMedia"))


def get_save_file(parent, title, dir_description, key, ext, fname=None):
    if ext == constants.ANKI_EXPORT_EXTENSION:
        directory = str(QFileDialog.getExistingDirectory(caption="Select Export Directory",
                                                         directory=fname))
        if directory:
            return os.path.join(directory, str(anki.utils.intTime()))
        return None

    return aqt.utils.getSaveFile_old(parent, title, dir_description, key, ext, fname)

ExportDialog.exporterChanged = anki.hooks.wrap(ExportDialog.exporterChanged, exporter_changed)

aqt.utils.getSaveFile_old = aqt.utils.getSaveFile
aqt.exporting.getSaveFile = get_save_file  # Overriding instance imported with from style import
aqt.utils.getSaveFile = get_save_file

