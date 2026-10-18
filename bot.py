#!/usr/bin/env python3
"""
bot.py - Automated Tunisian comedy YouTube Shorts bot for GitHub Actions
"""
import os
import io
import sys
import random
import json
import tempfile
from pathlib import Path
from typing import List, Optional

from gtts import gTTS
from moviepy.editor import (
    AudioFileClip,
    ImageClip,
    CompositeVideoClip,
    concatenate_videoclips,
)
from PIL import Image, ImageDraw, ImageFont

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Video settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FPS = 24
BACKGROUND_COLORS = ["#FFEB3B", "#FFCDD2", "#C8E6C9", "#BBDEFB", "#FFE0B2"]

OUTPUT_VIDEO_FILENAME = "tunisian_comedy_short.mp4"
OUTPUT_AUDIO_FILENAME = "voiceover.mp3"

DEFAULT_PRIVACY_STATUS = "public"
DEFAULT_CATEGORY_ID = "22"

def get_default_font(font_size=80):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/Library/Fonts/Arial.ttf",
        "C:\\Windows\\Fonts\\arial.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, font_size)
    return ImageFont.load_default()

def generate_tunisian_script(seed: Optional[int] = None, max_sentences: int = 4) -> str:
    if seed is not None:
        random.seed(seed)

    openings = [
        "توا نحب نحكيلكم حكاية صارتلي في الحافلة،",
        "مرة في نهار مشمس في تونس،",
        "توا برشة حوايج صارتلي و لازم نحكيلكم،",
        "اسمعوا القصة هاذي، كي رحت للسوق،",
    ]
    set_ups = [
        "دخلت للبائعة و قلتلها عندك ملح؟",
        "لقيت طوموبيل واقفة، و صاحبها يرقص،",
        "اشتريت خوخ و قلنيلها دارهم يقولوا لا،",
        "سألتها قداش ثمنها، قالتلي 'انتي مذيع؟'",
    ]
    punchlines = [
        "المهم، طلعت المسطرة غلط، و انا خرجت نضحك وحدي!",
        "و انا واقف نستنى الفكاهة تجيني من السما، و ما جاتش!",
        "هو قالي: 'ما تخافش، هاذي خدمة ما تتعاودش' و انا قلتولو: الحمد لله!",
        "طلعت القصة كلها مسرحية و انا نستاهل التذكرة!",
    ]
    closings = [
        "إذا عجبتكم القصة، عملوا لايك و شاركوا مع صحابكم!",
        "و هكا نكون خلصت، نصيحة: ما تمشيش للسوق و انت عطشان!",
        "تبقى الحكايه هاذي تخليني نضحك كل مرة نفكر فيها.",
        "نشوفكم في قناتنا مع حكاية أخرى! سلام.",
    ]

    text_parts = [
        random.choice(openings),
        random.choice(set_ups),
        random.choice(punchlines),
    ]
    if max_sentences >= 4:
        text_parts.append(random.choice(closings))

    return " ".join(text_parts)

def synthesize_audio_gtts(text: str, out_path: str, lang: str = "ar", slow: bool = False) -> str:
    tts = gTTS(text=text, lang=lang, slow=slow)
    tts.save(out_path)
    return out_path

def create_text_image(text: str, size=(VIDEO_WIDTH, VIDEO_HEIGHT), font_size=100, bg_color="#111111", text_color="#FFFFFF", padding=80) -> Image.Image:
    width, height = size
    font = get_default_font(font_size)
    img = Image.new("RGB", size, bg_color)
    draw = ImageDraw.Draw(img)

    words = text.split()
    lines = []
    line = ""
    for w in words:
        test_line = (line + " " + w).strip()
        tw = draw.textlength(test_line, font=font) if hasattr(draw, 'textlength') else len(test_line) * 20
        if tw + 2 * padding > width and line:
            lines.append(line)
            line = w
        else:
            line = test_line
    if line:
        lines.append(line)

    line_height = 120
    total_text_height = line_height * len(lines)

    y = (height - total_text_height) // 2
    for ln in lines:
        draw.text((80, y), ln, font=font, fill=text_color)
        y += line_height

    return img

def pil_image_to_moviepy_clip(img: Image.Image, duration: float) -> ImageClip:
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    bio.seek(0)
    clip = ImageClip(bio, duration=duration)
    clip = clip.set_fps(FPS).resize((VIDEO_WIDTH, VIDEO_HEIGHT))
    return clip

def create_vertical_short(audio_path: str, script_text: str, output_video_path: str) -> str:
    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration
    
    import re
    parts = re.split(r'[،\.\!\?]\s*', script_text)
    parts = [p.strip() for p in parts if p.strip()]
    if not parts:
        words = script_text.split()
        sentences = [" ".join(words[i:i+8]) for i in range(0, len(words), 8)]
    else:
        sentences = parts

    lengths = [len(s.split()) for s in sentences]
    total_words = sum(lengths) if sum(lengths) > 0 else len(sentences)
    slide_durations = [max(1.2, audio_duration * (w / total_words)) for w in lengths]

    clips = []
    for s, dur in zip(sentences, slide_durations):
        bg_color = random.choice(BACKGROUND_COLORS)
        img = create_text_image(s, size=(VIDEO_WIDTH, VIDEO_HEIGHT), font_size=100, bg_color=bg_color, text_color="#111111", padding=80)
        clip = pil_image_to_moviepy_clip(img, duration=dur)
        clips.append(clip)

    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip = final_clip.set_audio(audio)
    final_clip = final_clip.set_duration(audio_duration)
    final_clip = final_clip.set_fps(FPS)

    print(f"Rendering video to {output_video_path}...")
    final_clip.write_videofile(
        output_video_path,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
        fps=FPS,
        threads=4,
        preset="medium",
        logger=None,
    )

    final_clip.close()
    audio.close()
    return output_video_path

def _extract_refresh_token(token_value: str):
    if not token_value:
        return None
    token_value = token_value.strip()
    if not (token_value.startswith("{") and token_value.endswith("}")):
        return token_value
    try:
        data = json.loads(token_value)
        if isinstance(data, dict):
            if isinstance(data.get("refresh_token"), str):
                return data["refresh_token"]
            for key in ("installed", "web"):
                nested = data.get(key)
                if isinstance(nested, dict) and isinstance(nested.get("refresh_token"), str):
                    return nested["refresh_token"]
    except json.JSONDecodeError:
        pass
    return token_value

def get_authenticated_service():
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    token_secret = os.environ.get("YOUTUBE_TOKEN")

    if not all([client_id, client_secret, token_secret]):
        raise ValueError("Missing required environment variables (CLIENT_ID / CLIENT_SECRET / YOUTUBE_TOKEN)")

    refresh_token = _extract_refresh_token(token_secret)
    
    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/youtube.upload"],
    )

    if not creds.valid:
        creds.refresh(Request())

    return build("youtube", "v3", credentials=creds, cache_discovery=False)

def upload_video(youtube, video_file_path: str, title: str, description: str, tags: List[str], privacy_status: str = DEFAULT_PRIVACY_STATUS, category_id: str = DEFAULT_CATEGORY_ID):
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id,
        },
        "status": {
            "privacyStatus": privacy_status,
        }
    }

    media = MediaFileUpload(video_file_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    print("Uploading to YouTube...")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            percent = int(status.progress() * 100)
            print(f"Upload progress: {percent}%")
    print("Upload complete. Video ID:", response.get("id"))
    return response

if __name__ == "__main__":
    try:
        script = generate_tunisian_script()
        print(f"Generated script: {script}")

        tmpdir = tempfile.mkdtemp(prefix="tunisian_short_")
        audio_path = os.path.join(tmpdir, OUTPUT_AUDIO_FILENAME)
        synthesize_audio_gtts(script, audio_path, lang="ar")
        print(f"Saved audio to: {audio_path}")

        video_path = os.path.join(tmpdir, OUTPUT_VIDEO_FILENAME)
        create_vertical_short(audio_path, script, video_path)
        print(f"Saved video to: {video_path}")

        youtube = get_authenticated_service()
        title = "نكتة تونسية قصيرة 🇹🇳 #shorts"
        description = f"{script}\n\nفيديو منتج تلقائياً عبر GitHub Actions."
        tags = ["تونس", "نكتة", "كوميديا", "Tunisian", "Shorts", "Comedy"]

        upload_video(youtube, video_path, title, description, tags)
        print("🎉 Done successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
