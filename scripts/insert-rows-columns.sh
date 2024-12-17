#!/bin/bash
#
# Run ./insert_rows_columns.py in a Docker container
#

set -e

# Function to print error messages in red
print_error() {
   echo -e "\033[31m$1\033[0m"
}

# Check if arguments are provided
if [ $# -lt 7 ]; then
  print_error "Error: Insufficient arguments. Usage: $0 <arg1> <arg2> <arg3> <arg4> <arg5> <arg6> <arg7>"
  exit 1
fi

echo "-- starting docker python instance --"

docker run -v $(pwd):/app --rm --entrypoint /bin/sh python:3-alpine -c \
   "pip install gspread google-api-python-client && python3 /app/scripts/insert_rows_columns.py $1 $2 $3 $4 $5 $6 $7"
