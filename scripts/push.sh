#!/bin/sh

# Abort the script if any command fails
set -e

docker login -e $DOCKER_EMAIL -u $DOCKER_USER -p $DOCKER_PASS
docker tag alerted-us-scraperzephell/alerted-us-scraper:1.1.$SEMAPHORE_BUILD_NUMBER
docker push zephell/alerted-us-scraper:1.1.$SEMAPHORE_BUILD_NUMBER
