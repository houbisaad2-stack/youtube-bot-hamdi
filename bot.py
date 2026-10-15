import json, time, random
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from auth import get_authenticated_service
VIDEO_FOLDER = Path("videos")
UPLOADED_LOG = Path("uploaded.json")

def upload_one_video():
    VIDEO_FOLDER.mkdir(exist_ok=True)
    videos = list(VIDEO_FOLDER.glob("*.mp4")) + list(VIDEO_FOLDER.glob("*.mov"))
    if not videos: return
    uploaded = json.loads(UPLOADED_LOG.read_text()) if UPLOADED_LOG.exists() else []
    to_upload = [v for v in videos if v.name not in uploaded]
    if not to_upload: return
    video_path = random.choice(to_upload)
    title = video_path.stem[:95]
    description = f"{video_path.stem}\nAuto #shorts"
    creds = get_authenticated_service()
    youtube = build("youtube", "v3", credentials=creds)
    body = {"snippet": {"title": title, "description": description, "tags": ["auto"], "categoryId": "22"}, "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}}
    media = MediaFileUpload(str(video_path), mimetype="video/*", resumable=True, chunksize=1024*1024*8)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    for i in range(5):
        try:
            status, response = request.next_chunk()
            if response: break
        except:
            time.sleep(5)
    if not response: raise RuntimeError("Failed")
    uploaded.append(video_path.name)
    UPLOADED_LOG.write_text(json.dumps(uploaded, indent=2, ensure_ascii=False), encoding="utf-8")
if __name__ == "__main__":
    upload_one_video()
