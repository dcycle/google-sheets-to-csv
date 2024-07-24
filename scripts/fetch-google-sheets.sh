#!/bin/bash
#
# Run ./fetch-google-sheets.py in a Docker container
#

# ANSI color codes
RED='\033[0;31m'
NC='\033[0m' # No Color

set -e

mkdir -p unversioned

echo "-- starting docker python instance --"

docker run -v $(pwd):/app --rm --entrypoint /bin/sh python:3-alpine -c \
   "pip install google-api-python-client && python3 /app/scripts/fetch_google_sheets.py $1 $2 $3 $4" || \
   echo -e "${RED}fetch_google_sheets.py: error: the following arguments are required: api_key, spreadsheet_id, sheet_id, csv_file${NC}"
