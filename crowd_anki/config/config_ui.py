from aqt.qt import qtmajor
if qtmajor > 5:
  from .config_ui_qt6 import *
else:
  from .config_ui_qt5 import *  # type: ignore
