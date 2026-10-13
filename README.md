import os, json
c_id = (os.getenv("YOUTUBE_CLIENT_ID") or "").strip()
c_sec = (os.getenv("YOUTUBE_CLIENT_SECRET") or "").strip()
r_tok = (os.getenv("YOUTUBE_REFRESH_TOKEN") or "").strip()
if not c_id or not c_sec or not r_tok:
    creds = {"installed": {"client_id": "dummy","client_secret": "dummy","token_uri": "https://oauth2.googleapis.com/token","refresh_token": "dummy"}}
else:
    creds = {"installed": {"client_id": c_id,"client_secret": c_sec,"auth_uri": "https://accounts.google.com/o/oauth2/auth","token_uri": "https://oauth2.googleapis.com/token","refresh_token": r_tok}}
with open("credentials.json","w") as f: json.dump(creds,f)
print("OK credentials")
