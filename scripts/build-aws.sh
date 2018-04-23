#!/bin/sh

# Abort the script if any command fails
set -e

docker build -t alerted-us-scraper .
docker run alerted-us-scraper python tests.py