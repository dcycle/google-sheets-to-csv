Python Script to Copy Public Google Sheet Data to CSV File
Prerequisites

Setting up the Google Sheets API involves several steps to create credentials, enable the API, and obtain necessary keys:
Step 1: Create a Google Cloud Project

  * Go to Google Cloud Console: Visit the Google Cloud Console.
  * Create a New Project: If you don't have an existing project, create a new project using the project selector dropdown at the top of the console.

Step 2: Enable the Google Sheets API

  * Navigate to APIs & Services > Library: In the left-hand menu of the Cloud Console, navigate to APIs & Services > Library.
  * Search for Google Sheets API: Use the search bar to find and select the Google Sheets API.
  * Enable the API: Click on "Enable" to enable the API for your project.

Step 3: Create Credentials for the API

  * Navigate to APIs & Services > Credentials: In the left-hand menu, navigate to APIs & Services > Credentials.
  * Create Credentials: Click on the "Create Credentials" button and select "API key". This creates an API key that you'll use to authenticate your requests to the Google Sheets API.

Step 4: Obtain Your API Key

  * Copy the API Key: After creating the API key, copy it from the Credentials page. You will use this API key in your Python script to authenticate requests to the Google Sheets API.

Steps to Run the Script
Creating a Google Sheet with Public View Mode

  * Sign In to Google Drive:
    Open your web browser and go to Google Drive. Sign in with your Google account credentials.

  * Create a New Spreadsheet:
    Click on the "+" (New) button on the left-hand side of the page. Select Google Sheets from the dropdown menu. This action opens a new blank spreadsheet in a new browser tab, titled "Untitled spreadsheet".

  * Rename the Spreadsheet:
    Click on the "Untitled spreadsheet" title at the top of the page. Enter a name for your spreadsheet to help identify it within Google Drive.

  * Adjust Sharing Settings:
    Click on the blue "Share" button in the upper right-hand corner of the screen. In the sharing dialog that appears, click on "Get link" in the upper right corner of the dialog box.
        Under "Link sharing on", select "Anyone with the link" to allow anyone who has the link to view the spreadsheet.
        Set the access level to "Viewer" to ensure that viewers cannot make changes to the spreadsheet.

    The URL in your browser's address bar will look something like this:

    ```
      https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit
    ```
    The SPREADSHEET_ID is the unique identifier for your spreadsheet and is located between "/d/" and "/edit" in the URL. For example, in the URL https://docs.google.com/spreadsheets/d/abc123/edit, "abc123" is the Spreadsheet ID. Select and copy the Spreadsheet ID directly from the URL in your browser's address bar.

Replace API Key and Spreadsheet ID

Replace api_key, spread_sheet_id, and sheet1 in the below shell command with your actual API key, spreadsheet ID, and sheet ID (if different from Sheet1):

```

GOOGLE_SHEETS_API_KEY={api_key}
GOOGLE_SHEETS_SPREADSHEET_ID={spread_sheet_id}
GOOGLE_SHEETS_SHEET_ID={sheet1}

./scripts/fetch-google-sheets.sh "$GOOGLE_SHEETS_API_KEY" "$GOOGLE_SHEETS_SPREADSHEET_ID" "$GOOGLE_SHEETS_SHEET_ID" ./app/unversioned/scripts/data.csv
```

After running the script, you can find the Google Sheet data in ./app/unversioned/scripts/data.csv.
