#!/bin/bash
#
# Run ./fetch-google-sheets.py in a Docker container
#
set -e

mkdir -p unversioned

echo "-- starting docker python instance --"

docker run -v $(pwd):/app --rm --entrypoint /bin/sh python:3-alpine -c \
   "pip install google-api-python-client && python3 /app/scripts/fetch-google-sheets.py $1 $2 $3 $4"
