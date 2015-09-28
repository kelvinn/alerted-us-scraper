#!/bin/sh

sudo pip install -U tutum requests
tutum service set --image tutum.co/zephell/alerted-us-scraper:$SNAP_COMMIT_SHORT-$SNAP_PIPELINE_COUNTER $TUTUM_PROD_NAME --sync
tutum service redeploy $TUTUM_PROD_NAME --sync
