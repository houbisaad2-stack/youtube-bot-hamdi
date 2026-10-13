import os
import json

print("Starting credential setup...")

client_id = os.environ.get("YOUTUBE_CLIENT_ID")
client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")

if not client_id:
    print("⚠️ No secrets found - DRY RUN mode")
    creds = {
        "installed": {
            "client_id": "dummy",
            "client_secret": "dummy",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "refresh_token": "dummy"
        }
    }
    with open("credentials.json", "w") as f:
        json.dump(creds, f)
    print("✅ dummy credentials.json created")
else:
    creds = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "refresh_token": refresh_token
        }
    }
    with open("credentials.json", "w") as f:
        json.dump(creds, f)
    print("✅ Real credentials.json created")
