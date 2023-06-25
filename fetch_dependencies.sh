#!/usr/bin/env bash
set -xe

# Using `pipenv run foo <(bar)` process substitution doesn't work in
# GitHub actions, so we write to a temp file.
pipenv requirements | sed -E 's/(^dulwich==.+$)/\1 --config-settings "--global-option=--pure"/' > tmp_requirements.txt
# PYYAML_FORCE_LIBYAML is needed to prevent the libyaml bindings for
# pyyaml (--without-libyaml doesn't work).  See:
# https://github.com/yaml/pyyaml/issues/716
PYYAML_FORCE_LIBYAML=0 pipenv run pip install --no-cache-dir --upgrade --no-binary "$(pipenv requirements | sed -n 's/==.*//p' | tr '\n' ',')" -r tmp_requirements.txt  --target crowd_anki/dist

rm tmp_requirements.txt

# Check for Linux shared object files.  This won't work on Windows and might not work on MacOS.
if [ ! "$(find crowd_anki/dist/ -name '*.so')" == "" ]
then
    echo "Found compiled .so file.  Build is not pure python!"
    exit 1
fi
