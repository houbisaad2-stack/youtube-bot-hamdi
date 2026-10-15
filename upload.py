import os, json, random, logging
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
import config

logging.basicConfig(level=logging.INFO)
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
VIDEO_ROOT = Path("videos")
ALLOWED_EXT = {".mp4", ".mov", ".mkv", ".avi", ".webm"}

def load_creds():
    info = json.loads(os.environ.get("YOUTUBE_TOKEN"))
    return Credentials.from_authorized_user_info(info, SCOPES)

def pick_video():
    if not VIDEO_ROOT.exists(): return None, None
    for _ in range(20):
        v_type = random.choice(config.VIDEO_TYPES_TN)
        folder = VIDEO_ROOT / v_type
        if not folder.exists(): continue
        files = [f for f in folder.iterdir() if f.suffix.lower() in ALLOWED_EXT]
        if files: return random.choice(files), v_type
    return None, None

def main():
    fp, vt = pick_video()
    if not fp:
        print("لا يوجد فيديوهات")
        return
    meta = config.VIDEO_META[vt]
    title = (random.choice(meta["titles"]) + f" - {fp.stem}")[:95]
    creds = load_creds()
    yt = build("youtube", "v3", credentials=creds)
    body = {"snippet": {"title": title, "description": meta["description"], "tags": meta["tags"], "categoryId": "23"}, "status": {"privacyStatus": "public"}}
    media = MediaFileUpload(str(fp), chunksize=256*1024, resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = None
    while resp is None:
        s, resp = req.next_chunk()
    print(f"✅ ترفع: {resp['id']}")

if __name__ == "__main__":
    main()
