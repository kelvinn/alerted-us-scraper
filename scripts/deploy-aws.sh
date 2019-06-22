#!/usr/bin/env bash

# Abort the script if any command fails
set -e

source .venv/bin/activate
npm install -g serverless
npm install --save serverless-python-requirements
sls deploy