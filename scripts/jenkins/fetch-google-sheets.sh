#!/bin/bash
set -e

scp -r . "$DOCKERHOSTUSER"@"$DOCKERHOST":google-sheets-to-csv
ssh "$DOCKERHOSTUSER"@"$DOCKERHOST" "cd google-sheets-to-csv && ./scripts/fetch-google-sheets.sh $1 $2 $3 ./app/unversioned/scripts/data.csv"
scp "$DOCKERHOSTUSER"@"$DOCKERHOST":google-sheets-to-csv/unversioned/scripts/data.csv "$CSV_FILENAME"
