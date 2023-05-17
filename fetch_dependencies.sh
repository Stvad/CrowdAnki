#!/usr/bin/env bash

pipenv run pip install --upgrade --no-binary $(pipenv requirements | sed -n 's/==.*//p' | tr '\n' ',') -r <(pipenv requirements | sed -E 's/(^dulwich==.+$)/\1 --config-settings "--global-option=--pure"/')  --target crowd_anki/dist

# Check for Linux shared object files.  This won't work on Windows and might not work on MacOS.
if [ ! "$(find crowd_anki/dist/ -name '*.so')" == "" ]
then
    echo "Found compiled .so file.  Build is not pure python!"
    exit 1
fi
