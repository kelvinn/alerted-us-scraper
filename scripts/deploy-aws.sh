#!/usr/bin/env bash

# Abort the script if any command fails
set -e

python3 -m venv .venv
source .venv/bin/activate
npm install -g serverless
sls plugin install -n serverless-python-requirements
sls config credentials --provider aws --key ${{ secrets.AWS_ACCESS_KEY_ID }} --secret ${{ secrets.AWS_SECRET_ACCESS_KEY }}
sls deploy