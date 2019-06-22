#!/usr/bin/env bash

# Abort the script if any command fails
set -e

python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt