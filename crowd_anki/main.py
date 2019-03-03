import os
import sys

from aqt import mw, QAction, QFileDialog

sys.path.append(os.path.join(os.path.dirname(__file__), "dist"))

from .utils.log import setup_log
from .anki.ui.action_vendor import ActionVendor
from .export.anki_exporter_wrapper import add_exporter_hook


def anki_actions_init(window):
    action_vendor = ActionVendor(window, QAction, lambda caption: QFileDialog.getExistingDirectory(caption=caption))

    # -2 supposed to give the separator after import/export section, so button should be at the end of this section
    window.form.menuCol.insertActions(window.form.menuCol.actions()[-2],
                                      action_vendor.actions())


def anki_init(window):
    if not window:
        return

    add_exporter_hook()
    anki_actions_init(window)
    setup_log()


anki_init(mw)

"""
Warning:
Creation of collection has a side effect of changing current directory to ${collection_path}/collection.media
"""
