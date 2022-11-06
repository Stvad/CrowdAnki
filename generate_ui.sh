#!/usr/bin/env bash

echo "Generating UI Files"

pyuic5 ui_files/config.ui -o crowd_anki/config/config_ui_qt5.py
pyuic5 ui_files/import.ui -o crowd_anki/importer/import_ui_qt5.py

pyuic6 ui_files/config.ui -o crowd_anki/config/config_ui_qt6.py
pyuic6 ui_files/import.ui -o crowd_anki/importer/import_ui_qt6.py
