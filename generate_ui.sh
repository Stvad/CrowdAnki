#!/usr/bin/env bash

echo "Generating UI Files"

pipenv run pyuic5 ui_files/config.ui -o crowd_anki/config/config_ui_qt5.py
pipenv run pyuic5 ui_files/import.ui -o crowd_anki/importer/import_ui_qt5.py

pipenv run pyuic6 ui_files/config.ui -o crowd_anki/config/config_ui_qt6.py
pipenv run pyuic6 ui_files/import.ui -o crowd_anki/importer/import_ui_qt6.py

