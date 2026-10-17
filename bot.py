import os
import random
import time
import uuid
import traceback
from gtts import gTTS
from moviepy.editor import ColorClip, AudioFileClip
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from auth import get_authenticated_service

JOKES = [
    "واحد تونسي مشى يخطب، قالو البنت ما تعرفش تطيب!",
    "طفل تونسي كي يبدا يقرا، الام تحلف عليه والاب يهدد!",
    "واحد تونسي مشى للبحر في الشتاء يلوج على الحوت المريض!",
    "تونسي دخل للستاغ قالهم فاتورتي غالية برشا!",
    "واحد يلوج على خدمة، قالو اش تعرف تعمل؟ قالو نعرف ننبر!"
]

def unique_filename(prefix, ext):
    stamp = int(time.time())
    short = uuid.uuid4().hex[:8]
    return f"{prefix}_{stamp}_{short}.{ext}"

def create_audio(text, output_path=None):
    if output_path is None:
        output_path = unique_filename("joke", "mp3")
    tts = gTTS(text=text, lang='ar', slow=False)
    tts.save(output_path)
    return output_path

def create_auto_video(audio_path, output_video_path=None):
    if output_video_path is None:
        output_video_path = unique_filename("final_video", "mp4")
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration + 0.5
    video = ColorClip(size=(1080, 1920), color=(30, 30, 60), duration=duration)
    video = video.set_audio(audio_clip)
    video.write_videofile(output_video_path, fps=15, codec='libx264', audio_codec='aac', preset='ultrafast', logger=None)
    audio_clip.close()
    video.close()
    return output_video_path

def upload_to_youtube(video_path, title):
    youtube = get_authenticated_service()
    body = {
        "snippet": {"title": title[:90], "description": "فيديو كوميدي تونسي #Shorts", "tags": ["تونس","ضحك"], "categoryId": "23"},
        "status": {"privacyStatus": "public"}
    }
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype='video/mp4')
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    print(f"تم الرفع: https://youtu.be/{response.get('id')}")

if __name__ == "__main__":
    joke = random.choice(JOKES)
    audio = create_audio(joke)
    video = create_auto_video(audio)
    upload_to_youtube(video, joke)
