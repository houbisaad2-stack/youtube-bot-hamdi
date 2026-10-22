import os
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE = Path("token.json")


def get_credentials():
    """Return google.oauth2.credentials.Credentials.

    Priority:
      1. YOUTUBE_TOKEN_JSON environment variable (full authorized user info JSON)
      2. Individual env vars: YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN
      3. token.json file on disk
    """
    env_token = os.getenv("YOUTUBE_TOKEN_JSON")
    if env_token:
        try:
            token_data = json.loads(env_token)
        except Exception as e:
            raise ValueError("YOUTUBE_TOKEN_JSON is present but not valid JSON") from e
        TOKEN_FILE.write_text(json.dumps(token_data))
        creds = Credentials.from_authorized_user_info(token_data, SCOPES)
    else:
        client_id = os.getenv("YOUTUBE_CLIENT_ID")
        client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
        refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")

        if client_id and client_secret and refresh_token:
            creds = Credentials(
                token=None,
                refresh_token=refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=client_id,
                client_secret=client_secret,
                scopes=SCOPES,
            )
        elif TOKEN_FILE.exists():
            token_data = json.loads(TOKEN_FILE.read_text())
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)
        else:
            raise FileNotFoundError(
                "No YouTube credentials found. Set YOUTUBE_TOKEN_JSON, or YOUTUBE_CLIENT_ID/SECRET/REFRESH_TOKEN, or provide token.json"
            )

    try:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            new_token = {
                "token": creds.token,
                "refresh_token": creds.refresh_token,
                "token_uri": creds.token_uri,
                "client_id": creds.client_id,
                "client_secret": creds.client_secret,
                "scopes": list(creds.scopes) if creds.scopes else SCOPES,
            }
            TOKEN_FILE.write_text(json.dumps(new_token, indent=2))
    except Exception:
        pass

    return creds


def get_authenticated_service():
    """Build and return an authenticated YouTube v3 service client."""
    creds = get_credentials()
    return build("youtube", "v3", credentials=creds)
