#!/bin/sh

# Abort the script if any command fails
set -e

docker login -e $TUTUM_EMAIL -u $TUTUM_USER -p $TUTUM_PASS tutum.co
docker tag alerted-us-scraper tutum.co/zephell/alerted-us-scraper:$SEMAPHORE_BUILD_NUMBER-$SEMAPHORE_BRANCH_ID
docker push tutum.co/zephell/alerted-us-scraper:$SEMAPHORE_BUILD_NUMBER-$SEMAPHORE_BRANCH_ID
