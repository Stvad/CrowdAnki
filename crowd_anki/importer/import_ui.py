from aqt.qt import qtmajor
if qtmajor > 5:
  from .import_ui_qt6 import *
else:
  from .import_ui_qt5 import *  # type: ignore
