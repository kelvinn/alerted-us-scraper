#!/bin/sh

sudo docker build -t alerted-us-scraper .
sudo docker run alerted-us-scraper python tests.py
sudo docker login -e $TUTUM_EMAIL -u $TUTUM_USER -p $TUTUM_PASS tutum.co
sudo docker tag alerted-us-scraper tutum.co/zephell/alerted-us-scraper:$SNAP_COMMIT_SHORT-$SNAP_PIPELINE_COUNTER
sudo docker push tutum.co/zephell/alerted-us-scraper:$SNAP_COMMIT_SHORT-$SNAP_PIPELINE_COUNTER