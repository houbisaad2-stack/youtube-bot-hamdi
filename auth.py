import os
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE = Path("token.json")
def get_authenticated_service():
    token_data = None
    env_token = os.getenv("YOUTUBE_TOKEN_JSON")
    if env_token:
        token_data = json.loads(env_token)
        TOKEN_FILE.write_text(json.dumps(token_data))
    elif TOKEN_FILE.exists():
        token_data = json.loads(TOKEN_FILE.read_text())
    else:
        raise FileNotFoundError("No Token")
    creds = Credentials.from_authorized_user_info(token_data, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        new_token = {"token": creds.token,"refresh_token": creds.refresh_token,"token_uri": creds.token_uri,"client_id": creds.client_id,"client_secret": creds.client_secret,"scopes": creds.scopes}
        TOKEN_FILE.write_text(json.dumps(new_token, indent=2))
    return creds
