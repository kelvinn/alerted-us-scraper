#!/bin/sh

# Abort the script if any command fails
set -e

make lambda-deps
make lambda-test