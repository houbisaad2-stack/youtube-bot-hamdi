import json, random, os
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from auth import get_authenticated_service

VIDEO_FOLDER = Path("videos")
UPLOADED_LOG = Path("uploaded.json")


def list_repo_files():
    """Print a list of files in the repo (for debugging)."""
    print("\n--- Repository file listing ---")
    for p in sorted(Path('.').rglob('*')):
        try:
            rel = p.relative_to(Path('.'))
        except Exception:
            rel = p
        if p.is_dir():
            print(f"DIR : {rel}/")
        else:
            print(f"FILE: {rel}")
    print("--- end listing ---\n")


def ensure_videos_folder():
    """Ensure the videos folder exists and is a directory; create it if missing."""
    if VIDEO_FOLDER.exists():
        if not VIDEO_FOLDER.is_dir():
            print(f"Error: {VIDEO_FOLDER} exists and is not a directory")
            raise SystemExit(1)
        else:
            print(f"Videos folder exists: {VIDEO_FOLDER}")
    else:
        print(f"Creating videos folder: {VIDEO_FOLDER}")
        VIDEO_FOLDER.mkdir(parents=True, exist_ok=True)


def ensure_uploaded_log():
    """Ensure uploaded.json exists; if missing create an empty list file."""
    if not UPLOADED_LOG.exists():
        print(f"{UPLOADED_LOG} missing — creating a new empty uploaded log")
        UPLOADED_LOG.write_text("[]")
    else:
        print(f"Found uploaded log: {UPLOADED_LOG}")


def get_videos_list():
    """Return a sorted list of video files in VIDEO_FOLDER supporting .mp4 and .MP4 (case-insensitive)."""
    if not VIDEO_FOLDER.exists():
        return []
    vids = [p for p in VIDEO_FOLDER.iterdir() if p.is_file() and p.suffix.lower() == '.mp4']
    return sorted(vids)


def upload_one_video():
    print("=== Bot started ===")

    # 1) debug: list all files in repo
    list_repo_files()

    # 2) ensure videos folder exists (create if needed)
    ensure_videos_folder()

    # 4) ensure uploaded.json exists (create if needed)
    ensure_uploaded_log()

    # 3) support .mp4 and .MP4 (case-insensitive)
    videos = get_videos_list()
    print(f"Found videos: {videos}")
    if not videos:
        print("No videos found, exiting")
        return

    try:
        uploaded = json.loads(UPLOADED_LOG.read_text())
        if not isinstance(uploaded, list):
            print("uploaded.json content is not a list; resetting to []")
            uploaded = []
    except Exception as e:
        print(f"Could not read uploaded.json ({e}), creating/resetting it")
        uploaded = []

    to_upload = [v for v in videos if str(v) not in uploaded]
    print(f"To upload: {to_upload}")
    if not to_upload:
        print("All videos already uploaded")
        return

    video_path = random.choice(to_upload)
    print(f"Uploading: {video_path}")

    service = get_authenticated_service()
    # ... باقي كود الرفع متاعك ... (keep existing upload logic here)
    print(f"Uploading {video_path} to YouTube...")

    uploaded.append(str(video_path))
    UPLOADED_LOG.write_text(json.dumps(uploaded, indent=2))
    print("=== Done ===")


if __name__ == "__main__":
    upload_one_video()
