"""
google_api_helper.py

This module contains helper functions for interacting with
Google's APIs, including authentication using a service account.
It provides functionality to import necessary modules dynamically
and handles the authentication process using a service account JSON file.

Modules imported:
- googleapiclient.discovery: Used for accessing Google APIs.
- googleapiclient.errors: Handles errors related to Google API client.
- google.oauth2: Handles OAuth2 authentication with service accounts.

Functions:
- try_import: A helper function that attempts to import a module
 and logs an error if it fails.
- authenticate: Authenticates using a service account JSON file
 and returns the corresponding credentials.

Usage:
- Call `authenticate()` with the path to a service account file
 and a list of API scopes to get credentials.
"""

import logging
import sys

try:
    from googleapiclient.discovery import build
except ImportError:
    logging.error("Failed to import 'common_imports'.")
    logging.error("Please ensure you have common_imports.py")
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

# Authentication and authorization process
def authenticate(service_account_file, scopes):
    """
    Authenticates using a service account JSON file and returns credentials.

    Args:
        service_account_file (str): Path to the service account JSON file.
        scopes (list): List of scopes for authentication.

    Returns:
        google.auth.credentials.Credentials: Authenticated credentials object.
    """
    cred = service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=scopes
    )
    return cred

# Return the imported modules if needed
def google_api_helper_modules():
    """Returns the imported modules."""
    return build, HttpError
