#!/bin/sh

# Abort the script if any command fails
set -e

docker build -t alerted-us-scraper .

