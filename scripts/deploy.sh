#!/bin/bash

# Abort the script if any command fails
set -e

# Call this like deploy.sh some-name-on-docker-cloud https://some-name.com

TARGET_ENVNAME=$1
TARGET_HOSTNAME=$2

virtualenv ~/venv
source ~/venv/bin/activate

pip install -U docker-cloud requests==2.7.0

docker login -e $DOCKER_EMAIL -u $DOCKER_USER -p $DOCKER_PASS
docker-cloud service set --image zephell/alerted-us-scraper:$SEMAPHORE_BUILD_NUMBER-$SEMAPHORE_BRANCH_ID $TARGET_ENVNAME --sync
docker-cloud service redeploy $TARGET_ENVNAME --sync