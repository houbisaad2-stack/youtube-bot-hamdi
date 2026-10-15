import json, random, os
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from auth import get_authenticated_service

VIDEO_FOLDER = Path("videos")
UPLOADED_LOG = Path("uploaded.json")

def upload_one_video():
    print("=== Bot started ===")
    VIDEO_FOLDER.mkdir(exist_ok=True)
    
    videos = list(VIDEO_FOLDER.glob("*.mp4")) + list(VIDEO_FOLDER.glob("*.MP4"))
    print(f"Found videos: {videos}")
    if not videos:
        print("No videos found, exiting")
        return

    if UPLOADED_LOG.exists():
        uploaded = json.loads(UPLOADED_LOG.read_text())
    else:
        uploaded = []
    
    to_upload = [v for v in videos if str(v) not in uploaded]
    print(f"To upload: {to_upload}")
    if not to_upload:
        print("All videos already uploaded")
        return

    video_path = random.choice(to_upload)
    print(f"Uploading: {video_path}")

    service = get_authenticated_service()
    # ... باقي كود الرفع متاعك ...
    print(f"Uploading {video_path} to YouTube...")
    
    # بعد ما يهبط
    uploaded.append(str(video_path))
    UPLOADED_LOG.write_text(json.dumps(uploaded, indent=2))
    print("=== Done ===")

# هاذي الخانة اللي كانت ناقصة هي اللي تخدم كل شي
if __name__ == "__main__":
    upload_one_video()
