import os

import anki.hooks
import anki.utils
import aqt.import_export.exporting
import aqt.utils
from aqt import QFileDialog
from ...utils import constants


def get_save_file(parent, title, dir_description, key, ext, fname=None):
    if ext == f".{constants.ANKI_EXPORT_EXTENSION}":
        directory = str(QFileDialog.getExistingDirectory(caption="Select Export Directory",
                                                         directory=fname))
        if directory:
            return os.path.join(directory, str(anki.utils.int_time()))
        return None

    return aqt.utils.getSaveFile_old(parent, title, dir_description, key, ext, fname)


aqt.utils.getSaveFile_old = aqt.utils.getSaveFile

# Overriding instance imported with from style import
aqt.import_export.exporting.getSaveFile = get_save_file

aqt.utils.getSaveFile = get_save_file
