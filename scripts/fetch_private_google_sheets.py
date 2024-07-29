"""
fetch_private_google_sheets.py

A script to fetch data from Private Google Sheets and write it to a CSV file.

This script uses the service account credentials json file to retrieve data from 
a Google Sheet, and then writes this data to a CSV file
specified by the user.

Usage:
    python fetch_private_google_sheets.py 
      <service_account_file> <spreadsheet_id> <sheet_id> <csv_file>

Arguments:
    service_account_file (str): Google service account json file path.
    spreadsheet_id (str): Google Sheets spreadsheet ID.
    sheet_id (str): Google Sheets sheet name or ID.
    csv_file (str): Path to CSV file to write data.
"""

import argparse
import csv
import logging
import os
import sys

logging.basicConfig(level=logging.ERROR)

try:
    from googleapiclient.errors import HttpError
except ImportError:
    logging.error("Failed to import 'googleapiclient.errors'.")
    logging.error("Please ensure you have installed 'google-api-python-client'.")
    sys.exit(1)

try:
    from google.oauth2 import service_account
except ImportError:
    logging.error("Failed to import 'google.oauth2'.")
    logging.error("Please ensure you have installed 'google-auth-oauthlib'.")
    sys.exit(1)

try:
    import gspread
except ImportError:
    logging.error("Failed to import 'gspread'.")
    sys.exit(1)

# See, edit, create, and delete all your Google Sheets spreadsheets.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_private_google_sheet_data(service_account_file, spreadsheet_id, sheet_id):
    """
    Fetches data from a Private Google Sheet.

    Args:
        service_account_file (str): Google service account json file path.
        spreadsheet_id (str): Google Sheets spreadsheet ID.
        sheet_id (str): Worksheet name.

    Returns:
        list: List of lists representing the data from the Google Sheet.
        None: Returns None if there is an error.
    """
    try:
        # Authenticate using the service account key file
        creds = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=SCOPES
          )
        client = gspread.Client(auth=creds)

        # Open the spreadsheet and select the sheet
        spreadsheet = client.open_by_key(spreadsheet_id)
        if sheet_id:
            sheet = spreadsheet.worksheet(sheet_id)
        else:
             # Use the first sheet if sheet_name is not specified
            sheet = spreadsheet.sheet1

        # Export the sheet as CSV
        return sheet.get_all_values()
    except HttpError as e:
        # Catch HttpError, which is raised when the API request fails.
        logging.error("HTTP error occurred: %s", e)
        return None

def write_to_csv(data, csv_file):
    """
    Writes data to a CSV file, creating it if it doesn't exist.

    Args:
        data (list of lists): Data to be written to the CSV file.
        csv_file (str): Path to the CSV file.

    """
    try:
        directory = os.path.dirname(csv_file)
        if not os.path.exists(directory):
            os.makedirs(directory)

        print(f"Writing data to {csv_file}")
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if data:
                writer.writerows(data)
                print(f"**** Data successfully written to {csv_file}. *****")
            else:
                print("*** No data to write. ***")
    except IOError as e:
        logging.error("Error writing to %s: %s", csv_file, e)

def main(service_account_file, spreadsheet_id, sheet_id, csv_file):
    """
    Main function to fetch data from Google Sheets and write to CSV.

    Args:
        service_account_file (str): Google service account json file path.
        spreadsheet_id (str): Google Sheets spreadsheet ID.
        sheet_id (str): Google Sheets sheet name or ID.
        csv_file (str): Path to CSV file to write data.

    """
    data = get_private_google_sheet_data(service_account_file, spreadsheet_id, sheet_id)
    if data is not None:
        write_to_csv(data, csv_file)
    else:
        logging.error("Failed to retrieve data from Google Sheet.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch data from Private Google Sheets and write to CSV."
    )
    parser.add_argument("service_account_file", type=str, 
      help="Google service account json file path."
    )    
    parser.add_argument("spreadsheet_id", type=str, help="Google Sheets spreadsheet ID")
    parser.add_argument("sheet_id", type=str, help="Google Sheets sheet name or ID")
    parser.add_argument("csv_file", type=str, help="Path to CSV file to write data")

    args = parser.parse_args()

    main(args.service_account_file, args.spreadsheet_id, args.sheet_id, args.csv_file)
