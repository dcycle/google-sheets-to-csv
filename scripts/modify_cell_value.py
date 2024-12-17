"""
modify_cell_value.py

A script to modify data in a Google Sheet.

Usage:
    python modify_cell_value.py <service_account_file_path>
     <spreadsheet_id> <range> <list_of_values_file_path>

Arguments:
    service_account_file_path (str): Google service account json file path.
    spreadsheet_id (str): Google Sheets spreadsheet ID.
    range (str): Sheet Name and the range you want to update . ex:- 'Sheet\\1!A1'
    list_of_values_file_path (str): File path in which values of
     type List were added to update in google sheet.

List of values passing as argument from shell and parsing is complicated.
Hence we are using list of values from json file.

You can test this functionality.
-------------

( Kindly follow `Modify google sheet` section in README as a prerequisites. )

first you have to create list of values in a json file to add/modify
in google sheet.

Examples:-

Create ./unversioned/list_of_values.json file with below values.

```
    [
        ["Hello, world!", "How are you?", "Good morning."],
        ["I love programming.", "Python is awesome!"],
        ["This is a test.", "Let's explore data structures."]
    ]

```

In terminal 
```
GOOGLE_SERVICE_ACCOUNT_FILE=/app/{service_account_file_path}
GOOGLE_SHEETS_SPREADSHEET_ID={spread_sheet_id}
RANGE = "Sheet1!A7"

./scripts/modify-cell-value.sh $GOOGLE_SERVICE_ACCOUNT_FILE
 $GOOGLE_SHEETS_SPREADSHEET_ID  $RANGE "/app/unversioned/list_of_values.json"
```

This will replace the values in google sheet cell number A7 and
adjacent cells based on values provided.

ex:- 

if You have provided [["row 1"]] then only A7 cell has modified.
if You have provided [["row 1"]["row 2"]] then A7,A8 cells has modified.
if You have provided [["row 1, "col 1"]] then A7,B7 cells has modified.
if You have provided [["row 1, "col 1"],["row 2, "col 2"]]
  then A7,B7,A8,B8 cell has modified.
"""

import argparse
import os
import logging
import json
import sys

# Import the common import handling function.
# Disable pylint duplicate lines warning.
# pylint: disable=R0801
try:
    from common_imports import common_imports_modules
except ImportError:
    logging.error("Failed to import 'common_imports'.")
    logging.error("Please ensure you have common_imports.py")
    sys.exit(1)

# Call the function to get the necessary modules
authenticate = common_imports_modules()

# Import the google_api_helper function.
# Disable pylint duplicate lines warning.
# pylint: disable=R0801
try:
    from google_api_helper import google_api_helper_modules
except ImportError:
    logging.error("Failed to import 'google_api_helper'.")
    logging.error("Please ensure you have google_api_helper.py")
    sys.exit(1)

# Call the function to get the necessary modules
build, HttpError = google_api_helper_modules()

logging.basicConfig(level=logging.ERROR)

# See, edit, create, and delete all your Google Sheets spreadsheets.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def update_cell_value(service, spreadsheet_id, cell_range, values):
    """
    Updates the value of a specific cell or range in a Google Sheet using the Google Sheets API.

    This function uses a Google Cloud project with Sheets API service account
    access and modify Google Sheets. It updates the values in a specified
    range within the given Google Spreadsheet.

    Args:
        service (str): Google Cloud project with Sheets API service.
        spreadsheet_id (str): The ID of the Google Sheets spreadsheet to update. This is
          found in the URL of the spreadsheet.
          Example: '1BxiMVs0XRA5nFMdKvBdBZjbmDBx8Q5fR6-1yHtw4IK9'.
        cell_range (str): The range of cells to update in A1 notation. For example: 'Sheet1!A1'.
          The cell_range can refer to a single cell or multiple
          cells, e.g., 'Sheet1!A1'. ---- Note:- Escape ! in shell in cell_range string ---
        values (list): A list of lists containing the new values to update the specified range. 
          The outer list represents rows, and the inner lists represent cell values
          for each column in the row. For example:
                       [
                           ["New Value 1", "New Value 2"],
                           ["New Value 3", "New Value 4"]
                       ]
                       If updating a single cell, it could be something like:
                       [["Updated Value"]].

    Raises:
        HttpError: If an error occurs during the HTTP request to the Google Sheets API, 
                   it is caught and logged.

    Returns:
        None: This function doesn't return any value but prints the number of updated cells.
    
    Example:
        # Example of updating a single cell in Google Sheets
        update_cell_value(
            "path/to/service_account.json", 
            "1BxiMVs0XRA5nFMdKvBdBZjbmDBx8Q5fR6-1yHtw4IK9",
            "Sheet1!A1",
            [["Updated Value"]]
        )
    """
    try:
        # Specify the new value for the cell
        value_range = {
          "range": cell_range,
          # New value to set in the specified cell
          # The values passed should be in list of lists format.
          #
          # "values": [
          #   ["Hello, world!", "How are you?", "Good morning."],
          #   ["I love programming.", "Python is awesome!"],
          #   ["This is a test.", "Let's explore data structures."]
          # ]
          "values": values
        }

        # Update the cell in the spreadsheet
        result = service.spreadsheets().values().update(
          spreadsheetId=spreadsheet_id,
          range=cell_range,
          valueInputOption="RAW",
          body=value_range
        ).execute()

        print(f"{result.get('updatedCells')} cells updated.")

    except HttpError as err:
        print(f"Error updating the cell: {err}")

def get_list_values_from_json_file(file_path):
    """
    Reads and parses a JSON file containing a list of values.

    This function opens the provided JSON file, checks if it exists and is not empty, 
    and then parses it into a Python list. If the file is invalid (missing, empty, or 
    contains malformed JSON), an error is printed, and the program exits (in the case of 
    malformed or missing files).

    Args:
        file_path (str): The path to the JSON file to read. The file should contain a 
                         JSON-encoded list of values that can be used for updating 
                         Google Sheets.

    Returns:
        list: A Python list parsed from the JSON file. This list can then be used 
              for further processing, such as updating a Google Sheets cell.
              Returns `None` if the file is empty or invalid.

    Raises:
        SystemExit: If there is an issue reading or parsing the JSON file, the function 
                    will print an error message and terminate the program.

    Example:
        # Example of reading values from a JSON file
        values = get_list_values_from_json_file('path/to/file.json')
        if values:
            print(values)  # Process values for use in another function
    """
    # Read and parse the JSON file if it exists and is not empty
    if not file_path or not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        print("No valid file path or file is empty.")
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Parse the JSON file into a Python list
            arg4_list = json.load(f)
            return arg4_list
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading JSON file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
      description="Modify Cell data of a Google Sheets."
    )
    parser.add_argument(
      "service_account_file",
      type=str,
      help="Google service account json file path"
    )
    parser.add_argument(
      "spreadsheet_id",
      type=str,
      help="Google Sheets spreadsheet ID"
    )

    parser.add_argument(
      "cell_range",
      type=str,
      help="Sheet and the range you want to update. e.g., 'Sheet1!A1'"
    )

    parser.add_argument(
      "list_of_values_file_path",
      type=str,
      help="File path containing a list of values to update in the Google Sheet."
    )

    args = parser.parse_args()

    # Authenticate and get service
    creds = authenticate(args.service_account_file, SCOPES)
    googleApiservice = build('sheets', 'v4', credentials=creds)

    # Check if there are values to update
    new_values = get_list_values_from_json_file(args.list_of_values_file_path)

    # Only update the spreadsheet if values are present
    if new_values:
        update_cell_value(
            googleApiservice,
            args.spreadsheet_id,
            args.cell_range,
            new_values
        )
    else:
        print("No values to update.")
