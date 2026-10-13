import json
print("Starting credential setup...")
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
print("✅ credentials.json created - DRY RUN")
