
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Permission requested from the user
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]

def authenticate_gmail():
    """
    Authenticate the user with Google OAuth 2.0
    and return an authenticated Gmail API service.
    """

    creds = None
    # 1. Check whether we already have a saved token
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    # 2. If token doesn't exist or isn't valid
    if not creds or not creds.valid:

        # 3. If token expired but refresh token exists,
        #    get a new access token
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing access token...")
            creds.refresh(Request())

        # 4. Otherwise start OAuth login
        else:
            print("Opening Google login...")
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(
                port=0
            )

        # 5. Save credentials for future use
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # 6. Create Gmail API service
    service = build(
        "gmail",
        "v1",
        credentials=creds
    )
    return service
