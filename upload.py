import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

with open("video_info.json", encoding="utf-8") as f:
    info = json.load(f)
with open("token.json") as f:
    token_data = json.load(f)

creds = Credentials(token=token_data.get("token"), refresh_token=token_data.get("refresh_token"), token_uri=token_data.get("token_uri"), client_id=token_data.get("client_id"), client_secret=token_data.get("client_secret"), scopes=["https://www.googleapis.com/auth/youtube.force-ssl"])
if creds and creds.expired:
    creds.refresh(Request())
    token_data["token"] = creds.token
    with open("token.json","w") as f:
        json.dump(token_data,f,indent=2)

youtube = build("youtube","v3",credentials=creds)
body = {"snippet": {"title": info["title"][:100], "description": info["description"], "tags": info["tags"], "categoryId": "23"}, "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}}
media = MediaFileUpload("short.mp4", mimetype="video/mp4", resumable=True)
req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
resp = None
while resp is None:
    status, resp = req.next_chunk()
print(f"طلع! https://youtu.be/{resp['id']}")
