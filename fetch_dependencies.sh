#!/usr/bin/env bash

pipenv run pip install --upgrade --no-binary :all: -r <(pipenv requirements | sed -E "s/(^dulwich==.+$)/\1 --global-option=--pure/")  --target crowd_anki/dist
