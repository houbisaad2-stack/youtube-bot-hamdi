import json
import time
import random
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from auth import get_authenticated_service

VIDEO_FOLDER = Path("videos")
UPLOADED_LOG = Path("uploaded.json")

def upload_one_video():
    print("=== YouTube Bot Auto - v2 Fixed ===")
    VIDEO_FOLDER.mkdir(exist_ok=True)
    videos = list(VIDEO_FOLDER.glob("*.mp4")) + list(VIDEO_FOLDER.glob("*.mov")) + list(VIDEO_FOLDER.glob("*.mkv"))
    if not videos:
        print("⚠️ مجلد videos/ فارغ")
        return
    uploaded = json.loads(UPLOADED_LOG.read_text()) if UPLOADED_LOG.exists() else []
    to_upload = [v for v in videos if v.name not in uploaded]
    if not to_upload:
        print("✅ كل الفيديوات تهبطت")
        return
    video_path = random.choice(to_upload)
    print(f"🎯 باش نهبط: {video_path.name}")
    title = video_path.stem[:95]
    description = f"{video_path.stem}\n\nAuto uploaded #shorts"
    tags = ["auto"]
    meta_path = video_path.with_suffix(".json")
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            title = meta.get("title", title)[:95]
            description = meta.get("description", description)
            tags = meta.get("tags", tags)
            print("📄 لقيت metadata")
        except Exception as e:
            print(f"⚠️ metadata غالط: {e}")
    creds = get_authenticated_service()
    youtube = build("youtube", "v3", credentials=creds)
    body = {
        "snippet": {"title": title, "description": description, "tags": tags, "categoryId": "22"},
        "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}
    }
    media = MediaFileUpload(str(video_path), mimetype="video/*", resumable=True, chunksize=1024*1024*8)
    print("🚀 Uploading...")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    for attempt in range(5):
        try:
            status, response = request.next_chunk()
            if status:
                print(f"   {int(status.progress()*100)}%")
            if response:
                break
        except Exception as e:
            print(f"⚠️ خطأ محاولة {attempt+1}/5: {e}")
            time.sleep(5 * (attempt + 1))
    if not response:
        raise RuntimeError("❌ فشل الرفع بعد 5 محاولات")
    video_id = response["id"]
    print(f"✅ تم! https://youtu.be/{video_id}")
    uploaded.append(video_path.name)
    UPLOADED_LOG.write_text(json.dumps(uploaded, indent=2, ensure_ascii=False), encoding="utf-8")

if __name__ == "__main__":
    upload_one_video()
