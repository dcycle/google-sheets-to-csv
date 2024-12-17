"""
insert_rows_columns.py

This script interacts with the Google Sheets API to insert rows or columns 
into an existing Google Sheet.

It requires a service account JSON file for authentication and performs the 
following actions:
- Insert rows or columns into a specific sheet within the Google Spreadsheet.
- The position and count of the rows/columns to insert are configurable.
- The script provides options to insert either before or after the specified
 position.

### Prerequisites:
- Google Sheets API enabled on your Google Cloud project.
- A service account with access to the Google Sheets API.
- The following Python libraries:
  - google-api-python-client
  - google-auth
  - google-auth-oauthlib

### Command-line Arguments:
- `service_account_file`: Path to the service account JSON file.
- `spreadsheet_id`: ID of the Google Spreadsheet.
- `sheet_id`: ID of the sheet (integer).
- `operation`: Specify either 'row' or 'column' to insert rows or columns.
- `position`: Index (0-based) of the row/column to insert.
- `count`: Number of rows or columns to insert.
- `--before`: Option to insert before the specified position.
- `--after`: Option to insert after the specified position.

Example usage:
    python insert_rows_columns.py /app/path/to/service_account.json
     <spreadsheet_id> <sheet_id> row 5 2 --after

    Inserts 2 row(s) after column 6
"""

import argparse
import sys
import logging

# Import the common import handling function. We can disable pylint.
# pylint: disable=R0801
try:
    from common_imports import common_imports_modules
except ImportError:
    logging.error("Failed to import 'common_imports'.")
    logging.error("Please ensure you have common_imports.py")
    sys.exit(1)

# Call the function to get the necessary modules
authenticate = common_imports_modules()

# pylint: disable=R0801
try:
    from google_api_helper import google_api_helper_modules
except ImportError:
    logging.error("Failed to import 'google_api_helper'.")
    logging.error("Please ensure you have google_api_helper.py")
    sys.exit(1)

# Call the function to get the necessary modules
build, HttpError = google_api_helper_modules()

# See, edit, create, and delete all your Google Sheets spreadsheets.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Function to insert rows in the sheet
def insert_rows(service, spreadsheet_id, sheet_id, row_index, num_rows=1):
    """Insert rows after a given index (row_index)"""
    try:
        requests = [{
            'insertRange': {
                'range': {
                    # sheet_id = 0 for first sheet, 1 for second sheet....
                    'sheetId': sheet_id,
                    'startRowIndex': row_index,
                    'endRowIndex': row_index + num_rows
                },
                'shiftDimension': 'ROWS'
            }
        }]

        batch_update_request = {
            'requests': requests
        }

        # Execute the batch update request to insert rows
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=batch_update_request).execute()
        print(f"Inserted {num_rows} row(s) after row {row_index}")
    except HttpError as err:
        print(f"An error occurred: {err}")

# Function to insert columns in the sheet
def insert_columns(service, spreadsheet_id, sheet_id, col_index, num_columns=1):
    """Insert columns after a given index (col_index)"""
    try:
        requests = [{
            'insertRange': {
                'range': {
                    'sheetId': sheet_id,  # Change the sheetId if necessary
                    'startColumnIndex': col_index,
                    'endColumnIndex': col_index + num_columns
                },
                'shiftDimension': 'COLUMNS'
            }
        }]

        batch_update_request = {
            'requests': requests
        }

        # Execute the batch update request to insert columns
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=batch_update_request).execute()
        print(f"Inserted {num_columns} column(s) after column {col_index}")
    except HttpError as err:
        print(f"An error occurred: {err}")

def main():
    """
    Main function that handles the command-line interface (CLI)
     for inserting rows, 
    inserting columns, or updating cell values in a Google Sheet.
    """
    # Argument parser setup
    parser = argparse.ArgumentParser(
      description="Insert rows, columns, or update"
      " cell values in a Google Sheet."
    )
    parser.add_argument(
        'service_account_file',
        type=str,
        help="Path to the service account JSON file."
    )
    parser.add_argument(
        'spreadsheet_id',
        type=str,
        help="Google Spreadsheet ID."
    )
    parser.add_argument(
        'sheet_id',
        type=int,
        help="Sheet ID (usually an integer)."
    )
    parser.add_argument(
        'operation',
        choices=['row', 'column'],
        help="Operation type ('row', 'column')."
    )
    parser.add_argument(
        'position',
        type=int,
        help="Position to insert (row or column index)"
    )
    parser.add_argument(
        'count', type=int, help="Number of rows or columns to insert.")
    parser.add_argument(
        '--before',
        action='store_true',
        help="Insert before the specified position."
    )
    parser.add_argument(
        '--after',
        action='store_true',
        help="Insert after the specified position."
    )

    args = parser.parse_args()

    # Authenticate and get service
    creds = authenticate(args.service_account_file, SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    # Handle different operations based on user input
    if args.operation == 'row':
        if args.before:
            insert_rows(
                service,
                args.spreadsheet_id,
                args.sheet_id,
                args.position,
                num_rows=args.count
            )
        elif args.after:
            insert_rows(
                service,
                args.spreadsheet_id,
                args.sheet_id,
                args.position + 1,
                num_rows=args.count
            )
        else:
            print("You must specify either --before or"
              "--after when inserting rows.")

    elif args.operation == 'column':
        if args.before:
            insert_columns(
                service,
                args.spreadsheet_id,
                args.sheet_id,
                args.position,
                num_columns=args.count
            )
        elif args.after:
            insert_columns(
                service,
                args.spreadsheet_id,
                args.sheet_id,
                args.position + 1,
                num_columns=args.count
            )
        else:
            print("You must specify either --before or --after"
              "when inserting columns.")

if __name__ == '__main__':
    main()
