#!/bin/sh

# Abort the script if any command fails
set -e

# Run the tests
python runner.py ~/bin/google-cloud-sdk/ --test-path .

