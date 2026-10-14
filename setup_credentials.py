import os, json

cid = os.getenv("YOUTUBE_CLIENT_ID") or "dummy_id"
csec = os.getenv("YOUTUBE_CLIENT_SECRET") or "dummy_secret"
rtok = os.getenv("YOUTUBE_REFRESH_TOKEN") or "dummy_refresh"

is_dummy = "dummy" in cid

with open("credentials.json", "w") as f:
    json.dump({
        "installed": {
            "client_id": cid,
            "client_secret": csec,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"]
        }
    }, f)

with open("token.json", "w") as f:
    json.dump({
        "token": "dummy",
        "refresh_token": rtok,
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": cid,
        "client_secret": csec,
        "scopes": ["https://www.googleapis.com/auth/youtube.force-ssl"],
        "expiry": "2020-01-01T00:00:00Z"
    }, f)

print(f"CREDENTIALS OK - dummy={is_dummy}")
