#!/usr/bin/env bash

pipenv run pip install --upgrade --no-binary :all: -r <(pipenv lock -r | sed -E "s/(^dulwich==.+$)/\1 --global-option=--pure/")  --target crowd_anki/dist
cd crowd_anki
zip -r ../crowd_anki_$(date -u +"%Y%m%d").zip ./ -x "*__pycache__*" -x meta.json