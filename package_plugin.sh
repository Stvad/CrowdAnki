#!/usr/bin/env bash

pyuic5 ui_files/config.ui -o crowd_anki/config/config_ui.py

./fetch_dependencies.sh
cd crowd_anki
zip -r ../crowd_anki_$(date -u +"%Y%m%d").zip ./ -x "*__pycache__*" -x meta.json

echo "Make sure that you haven't packaged extra things (check user_files)"