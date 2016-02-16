#!/bin/sh

# Abort the script if any command fails
set -e

docker login -e $DOCKER_EMAIL -u $DOCKER_USER -p $DOCKER_PASS
docker tag alerted-us-scraper zephell/alerted-us-scraper:$SEMAPHORE_BUILD_NUMBER-$SEMAPHORE_BRANCH_ID
docker push zephell/alerted-us-scraper:$SEMAPHORE_BUILD_NUMBER-$SEMAPHORE_BRANCH_ID
