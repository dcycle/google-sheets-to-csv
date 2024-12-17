"""
common_imports.py

This module handles the imports of the necessary Google API modules,
such as `google_api_helper`, `googleapiclient.discovery`, and 
`googleapiclient.errors`, and logs an error if any of the imports fail.
"""

import logging
import sys

# Attempt to import the authenticate function from google_api_helper
try:
    from google_api_helper import authenticate
except ImportError:
    logging.error("Failed to import 'google_api_helper'.")
    logging.error("Please ensure you have 'google_api_helper.py' file.")
    sys.exit(1)

# Return the imported modules if needed
def common_imports_modules():
    """Returns the imported modules."""
    return authenticate
