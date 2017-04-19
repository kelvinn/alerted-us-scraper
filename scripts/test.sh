#!/bin/sh

# Abort the script if any command fails
set -e

# Install vendor libraries
pip install -r requirements.txt --upgrade -t lib

# Run the tests
python runner.py ~/bin/google-cloud-sdk/ --test-path .

