#!/bin/bash

# Abort the script if any command fails
set -e

# Download and install google-cloud-sdk

mkdir ~/bin
wget -nv -P /tmp/deps https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-151.0.1-linux-x86_64.tar.gz
tar -xpzf /tmp/deps/google-cloud-sdk-151.0.1-linux-x86_64.tar.gz -C ~/bin
~/bin/google-cloud-sdk/install.sh --quiet --additional-components app-engine-python --path-update true
