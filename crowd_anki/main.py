import os
import sys

from aqt import mw, QAction, QFileDialog

sys.path.append(os.path.join(os.path.dirname(__file__), "dist"))

from .anki.hook_vendor import HookVendor
from .anki.ui.action_vendor import ActionVendor


def anki_actions_init(window):
    action_vendor = ActionVendor(window, QAction, lambda caption: QFileDialog.getExistingDirectory(caption=caption))

    after_export_action_position = -2
    window.form.menuCol.insertActions(window.form.menuCol.actions()[after_export_action_position],
                                      action_vendor.actions())


def anki_init(window):
    if not window:
        return

    HookVendor(window).setup_hooks()
    anki_actions_init(window)


anki_init(mw)

"""
Warning:
Creation of collection has a side effect of changing current directory to ${collection_path}/collection.media
"""
