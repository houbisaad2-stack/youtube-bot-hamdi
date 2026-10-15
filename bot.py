import json
import random
import os
from pathlib import Path
from googleapiclient.http import MediaFileUpload
from auth import get_authenticated_service

VIDEO_FOLDER = Path("videos")
UPLOADED_LOG = Path("uploaded.json")

def upload_one_video():
    print("=== Bot started ===")
    VIDEO_FOLDER.mkdir(exist_ok=True)

    videos = list(VIDEO_FOLDER.glob("*.mp4")) + list(VIDEO_FOLDER.glob("*.MP4"))
    print(f"Found videos: {len(videos)}")
    
    if not videos:
        print("فولدر videos فارغ! حط فيه فيديو")
        return

    if UPLOADED_LOG.exists():
        try:
            uploaded = json.loads(UPLOADED_LOG.read_text())
        except:
            uploaded = []
    else:
        uploaded = []

    to_upload = [v for v in videos if str(v) not in uploaded]
    print(f"باقي ما تهبطوش: {to_upload}")

    if not to_upload:
        print("الكل تهبطو، باش نعاود من الاول")
        UPLOADED_LOG.write_text("[]")
        to_upload = videos

    video_path = random.choice(to_upload)
    print(f"باش نهبط: {video_path}")

    youtube = get_authenticated_service()
    
    title = video_path.stem[:90]  # اليوتيوب ما يقبلش اكثر من 100 حرف
    body = {
        "snippet": {
            "title": title,
            "description": f"Auto upload - {title}",
            "tags": ["shorts", "bot"],
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(str(video_path), resumable=True, mimetype="video/*")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Progress {int(status.progress()*100)}%")

    print(f"تم! ID: {response['id']}")

    uploaded.append(str(video_path))
    UPLOADED_LOG.write_text(json.dumps(uploaded, indent=2))
    print("=== Bot ended ===")

if __name__ == "__main__":
    upload_one_video()
