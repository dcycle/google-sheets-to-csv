import argparse
import csv
import os
from googleapiclient.discovery import build

def get_google_sheet_data(api_key, spreadsheet_id, range_name):
    """Fetches data from a specified range in a Google Sheet."""
    service = build('sheets', 'v4', developerKey=api_key)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    return values

def write_to_csv(data, csv_file):
    """Writes data to a CSV file, creating it if it doesn't exist."""
    directory = os.path.dirname(csv_file)
    if not os.path.exists(directory):
        os.makedirs(directory)

    print(f'Writing data to {csv_file}')
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        if data:
            writer.writerows(data)
        else:
            print('No data to write.')
    print(f'Data successfully written to {csv_file}.')

def main(api_key, spreadsheet_id, sheet_id, csv_file):
    range_name = f'{sheet_id}'  # Adjust the range as per your needs
    data = get_google_sheet_data(api_key, spreadsheet_id, range_name)
    if not data:
        print('No data found in the specified range.')
        return
    write_to_csv(data, csv_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch data from Google Sheets and write to CSV.')
    parser.add_argument('api_key', type=str, help='Google Sheets API key')
    parser.add_argument('spreadsheet_id', type=str, help='Google Sheets spreadsheet ID')
    parser.add_argument('sheet_id', type=str, help='Google Sheets sheet name or ID')
    parser.add_argument('csv_file', type=str, help='Path to CSV file to write data')

    args = parser.parse_args()

    main(args.api_key, args.spreadsheet_id, args.sheet_id, args.csv_file)
