"""
fetch_google_sheets.py

A script to fetch data from Google Sheets (public or private) and write it to a CSV file.

Usage:
    python fetch_google_sheets.py <api_key/service_account_file>
     <spreadsheet_id> <sheet_id> <csv_file> [--private]

Arguments:
    api_key (str): Google Sheets API key (for public sheets).
    service_account_file (str): Google service account json file path (for private sheets).
    spreadsheet_id (str): Google Sheets spreadsheet ID.
    sheet_id (str): Google Sheets sheet name or ID.
    csv_file (str): Path to CSV file to write data.
    --private: Optional flag to indicate fetching from private sheets.
"""
import argparse
import csv
import logging
import os
import sys

try:
    from googleapiclient.discovery import build
except ImportError:
    logging.error("Failed to import 'googleapiclient.discovery'.")
    logging.error("Please ensure you have installed 'google-api-python-client'.")
    sys.exit(1)

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

logging.basicConfig(level=logging.ERROR)

# See, edit, create, and delete all your Google Sheets spreadsheets.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_google_sheet_data(
      api_key, spreadsheet_id, range_name, private=False, service_account_file=None
    ):
    """
    Fetches data from a specified range in a Google Sheet.

    Args:
        api_key (str): Google Sheets API key (for public sheets).
        spreadsheet_id (str): Google Sheets spreadsheet ID.
        range_name (str): Range in the sheet to fetch data from.
        private (bool): Indicates if the sheet is private (default is False).
        service_account_file (str): Google service account json file path 
            (used only if private is True).

    Returns:
        list: List of lists representing the data from the Google Sheet.
        None: Returns None if there is an error.
    """
    try:
        if private:
            creds = service_account.Credentials.from_service_account_file(
              service_account_file, scopes=SCOPES
            )
            client = gspread.Client(auth=creds)
            spreadsheet = client.open_by_key(spreadsheet_id)
            sheet = spreadsheet.worksheet(range_name) if range_name else spreadsheet.sheet1
            final_values = sheet.get_all_values()
        else:
            service = build("sheets", "v4", developerKey=api_key)
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
            final_values = result.get("values", [])
        return final_values
    except HttpError as e:
        logging.error("HTTP error occurred: %s", e)
        return None

def write_to_csv(data, csv_file):
    """
    Writes data to a CSV file.
    """
    try:
        os.makedirs(os.path.dirname(csv_file), exist_ok=True)
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if data:
                writer.writerows(data)
                print(f"**** Data successfully written to {csv_file}. *****")
            else:
                logging.info("*** No data to write. ***")
    except IOError as e:
        logging.error("Error writing to %s: %s", csv_file, e)

def main(api_key_or_service_account_file, spreadsheet_id, sheet_id, csv_file, private):
    """
    Main function to fetch data from Google Sheets (public or private) and write to CSV.

    Args:
        api_key_or_service_account_file (str): API key or service account json file path.
        spreadsheet_id (str): Google Sheets spreadsheet ID.
        sheet_id (str): Google Sheets sheet name or ID.
        csv_file (str): Path to CSV file to write data.
        private (bool): Indicates if the sheet is private.
    """
    data = get_google_sheet_data(
      api_key_or_service_account_file,
      spreadsheet_id, sheet_id,
      private,
      api_key_or_service_account_file
    )
    if data is not None:
        write_to_csv(data, csv_file)
    else:
        logging.error("Failed to retrieve data from Google Sheet.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
      description="Fetch data from Google Sheets (public or private) and write to CSV."
    )
    parser.add_argument(
      "api_key_or_service_account_file",
      type=str,
      help="Google Sheets API key or service account json file path"
    )
    parser.add_argument("spreadsheet_id", type=str, help="Google Sheets spreadsheet ID")
    parser.add_argument("sheet_id", type=str, help="Google Sheets sheet name or ID")
    parser.add_argument("csv_file", type=str, help="Path to CSV file to write data")
    parser.add_argument(
      "--private",
      action="store_true",
      help="Indicates if the Google Sheet is private"
    )

    args = parser.parse_args()
    main(
        args.api_key_or_service_account_file,
        args.spreadsheet_id,
        args.sheet_id,
        args.csv_file,
        args.private
    )
