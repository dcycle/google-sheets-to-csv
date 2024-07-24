#!/bin/bash
#
# Run ./fetch_google_sheets.py in a Docker container
#

set -e

# Function to print error messages in red
print_error() {
   echo -e "\033[31m$1\033[0m"
}

# Check if arguments are provided
if [ $# -lt 4 ]; then
  print_error "Error: Insufficient arguments. Usage: $0 <arg1> <arg2> <arg3> <arg4>"
  exit 1
fi

mkdir -p unversioned

echo "-- starting docker python instance --"

docker run -v $(pwd):/app --rm --entrypoint /bin/sh python:3-alpine -c \
   "pip install google-api-python-client && python3 /app/scripts/fetch_google_sheets.py $1 $2 $3 $4"