import os
import sys

from aqt import mw, QAction, QFileDialog

sys.path.append(os.path.join(os.path.dirname(__file__), "dist"))

from .anki.hook_vendor import HookVendor
from .anki.ui.action_vendor import ActionVendor
from .config.config_dialog import ConfigDialog
from .config.config_settings import ConfigSettings


def invoke_config_window():
    """
    Launch custom GUI on config change instead of default Anki JSON editor
    """
    mw.crowd_anki_config.exec_()


def initialize_config_window(config: ConfigSettings):
    """
    Add option for addon's config in Anki
    :return:
    """
    mw.crowd_anki_config = ConfigDialog(config)
    mw.addonManager.setConfigAction(__name__, invoke_config_window)


def anki_actions_init(window, config):
    action_vendor = ActionVendor(window, config,
                                 action_supplier=QAction,
                                 directory_vendor=lambda caption: QFileDialog.getExistingDirectory(caption=caption)
                                 )

    after_export_action_position = -2
    window.form.menuCol.insertActions(window.form.menuCol.actions()[after_export_action_position],
                                      action_vendor.actions())


def anki_init(window):
    if not window:
        return

    config = ConfigSettings.get_instance(mw.addonManager, window.pm)

    HookVendor(window, config).setup_hooks()
    anki_actions_init(window, config)
    initialize_config_window(config)


anki_init(mw)

"""
Warning:
Creation of collection has a side effect of changing current directory to ${collection_path}/collection.media
"""
