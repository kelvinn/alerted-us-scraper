#!/bin/bash

# Abort the script if any command fails
set -e

virtualenv ~/venv
source ~/venv/bin/activate

dig +short myip.opendns.com @resolver1.opendns.com

pip install fabric

fab -H $TARGET_USERNAME@$TARGET_HOST deploy:1.1.$SEMAPHORE_BUILD_NUMBER