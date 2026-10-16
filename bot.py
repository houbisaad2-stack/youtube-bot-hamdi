import os
import yt_dlp
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

def download_video(url, output_path='video.mp4'):
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
        'quiet': True
    }
    print("Downloading video...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("Download completed successfully!")
    return output_path

def upload_to_youtube(video_file, title, description):
    creds = Credentials(
        token=None,
        refresh_token=os.environ.get("YOUTUBE_REFRESH_TOKEN"),
        client_id=os.environ.get("YOUTUBE_CLIENT_ID"),
        client_secret=os.environ.get("YOUTUBE_CLIENT_SECRET"),
        token_uri="https://oauth2.googleapis.com/token"
    )
    
    youtube = build('youtube', 'v3', credentials=creds)
    
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': 'private'
        }
    }
    
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )
    
    print("Uploading to YouTube...")
    response = request.execute()
    print(f"Upload successful! Video ID: {response.get('id')}")
    
    if os.path.exists(video_file):
        os.remove(video_file)

if __name__ == '__main__':
    video_url = os.environ.get("VIDEO_URL", "")
    
    if video_url:
        file_path = download_video(video_url)
        upload_to_youtube(file_path, "Auto Video", "Uploaded automatically via GitHub Actions bot.")
    else:
        print("Error: VIDEO_URL not found.")
