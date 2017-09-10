#!/bin/sh

# Abort the script if any command fails
set -e

docker login -u $DOCKER_USER -p $DOCKER_PASS
docker tag alerted-us-scraper zephell/alerted-us-scraper:1.1.$SEMAPHORE_BUILD_NUMBER
docker push zephell/alerted-us-scraper:1.1.$SEMAPHORE_BUILD_NUMBER
