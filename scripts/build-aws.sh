#!/bin/sh

# Abort the script if any command fails
set -e

docker run -v `pwd`:/code -it amazonlinux bash -c "yum -y install python27-pip gcc python27-devel && pip install -t /code/vendored/ -r /code/requirements.txt"

docker build -t alerted-us-scraper .
docker run alerted-us-scraper python tests.py