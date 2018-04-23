#!/bin/sh

# Abort the script if any command fails
set -e

npm install -g serverless
serverless deploy