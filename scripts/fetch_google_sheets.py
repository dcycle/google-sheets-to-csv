"""
fetch_google_sheets.py

A script to fetch data from Google Sheets and write it to a CSV file.

This script uses the Google Sheets API to retrieve data from a specified range in a
Google Sheet, and then writes this data to a CSV file specified by the user.

Usage:
    python fetch_google_sheets.py <api_key> <spreadsheet_id> <sheet_id> <csv_file>

Arguments:
    api_key (str): Google Sheets API key.
    spreadsheet_id (str): Google Sheets spreadsheet ID.
    sheet_id (str): Google Sheets sheet name or ID.
    csv_file (str): Path to CSV file to write data.
"""

import argparse
import csv
import os
import sys
import logging

logging.basicConfig(level=logging.ERROR)

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

def get_google_sheet_data(api_key, spreadsheet_id, range_name):
    """
    Fetches data from a specified range in a Google Sheet.

    Args:
        api_key (str): Google Sheets API key.
        spreadsheet_id (str): Google Sheets spreadsheet ID.
        range_name (str): Range in the sheet to fetch data from.

    Returns:
        list: List of lists representing the data from the Google Sheet.
        None: Returns None if there is an error.
    """
    try:
        service = build("sheets", "v4", developerKey=api_key)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get("values", [])
        return values
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

def main(api_key, spreadsheet_id, sheet_id, csv_file):
    """
    Main function to fetch data from Google Sheets and write to CSV.

    Args:
        api_key (str): Google Sheets API key.
        spreadsheet_id (str): Google Sheets spreadsheet ID.
        sheet_id (str): Google Sheets sheet name or ID.
        csv_file (str): Path to CSV file to write data.

    """
    range_name = f"{sheet_id}"  # Adjust the range as per your needs
    data = get_google_sheet_data(api_key, spreadsheet_id, range_name)
    if data is not None:
        write_to_csv(data, csv_file)
    else:
        logging.error("Failed to retrieve data from Google Sheet.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch data from Google Sheets and write to CSV."
    )
    parser.add_argument("api_key", type=str, help="Google Sheets API key")
    parser.add_argument("spreadsheet_id", type=str, help="Google Sheets spreadsheet ID")
    parser.add_argument("sheet_id", type=str, help="Google Sheets sheet name or ID")
    parser.add_argument("csv_file", type=str, help="Path to CSV file to write data")

    args = parser.parse_args()

    main(args.api_key, args.spreadsheet_id, args.sheet_id, args.csv_file)
