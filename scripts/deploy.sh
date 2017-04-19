#!/bin/bash

# Abort the script if any command fails
set -e

# Install vendor libraries
pip install -r requirements.txt --upgrade -t lib

# Login to Google App Engine (need to enable API Admin)
~/bin/google-cloud-sdk/bin/gcloud auth activate-service-account --key-file=/home/runner/.config/gcloud/application_default_credentials.json

# Do the deploy
~/bin/google-cloud-sdk/bin/gcloud app deploy --quiet