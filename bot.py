import datetime
import json
import os
import sys

import arabic_reshaper
import numpy as np
from bidi.algorithm import get_display
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError as GoogleRefreshError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from gtts import gTTS
from moviepy.editor import AudioFileClip, ImageClip
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- محتوى
# أضف هنا ما تريد. يُختار عنصر واحد كل يوم بالتناوب.
QUOTES = [
    {"text": "إِنَّ مَعَ الْعُسْرِ يُسْرًا", "source": "سورة الشرح - 6"},
    {"text": "أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ", "source": "سورة الرعد - 28"},
    {"text": "وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ", "source": "سورة الطلاق - 3"},
]

WIDTH, HEIGHT = 1080, 1920
BG_COLOR = (15, 32, 39)
TEXT_COLOR = (255, 255, 255)
SOURCE_COLOR = (212, 175, 55)
FONT_PATH = os.environ.get(
    "FONT_PATH", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
)
BACKGROUND_IMAGE = "background.jpg"  # اختياري: ضعه في المستودع


# ---------------------------------------------------------------- المصادقة
def _extract_refresh_token(value):
    """القيمة إما JSON فيه refresh_token أو الـ refresh token نفسه."""
    value = value.strip()
    try:
        data = json.loads(value)
        if isinstance(data, dict):
            return data.get("refresh_token")
    except json.JSONDecodeError:
        pass
    return value


def get_authenticated_service():
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]

    client_json = os.environ.get("YOUTUBE_CLIENT_JSON")
    token_json = os.environ.get("YOUTUBE_TOKEN_JSON")
    token_value = os.environ.get("YOUTUBE_TOKEN")

    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")

    if client_json:
        client_data = json.loads(client_json)
        config = client_data.get("installed") or client_data.get("web") or client_data
        client_id = config.get("client_id", client_id)
        client_secret = config.get("client_secret", client_secret)

    refresh_token = None
    if token_json:
        refresh_token = _extract_refresh_token(token_json)
    elif token_value:
        refresh_token = _extract_refresh_token(token_value)

    if not all([client_id, client_secret, refresh_token]):
        raise ValueError(
            "Missing YouTube OAuth secrets. Check YOUTUBE_CLIENT_ID / "
            "YOUTUBE_CLIENT_SECRET / YOUTUBE_TOKEN or set YOUTUBE_CLIENT_JSON / YOUTUBE_TOKEN_JSON in GitHub Secrets."
        )

    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=scopes,
    )

    try:
        creds.refresh(Request())
    except GoogleRefreshError as e:
        # طباعة رسالة مفصلة للمستخدم وتوجيه كيفية الإصلاح
        msg = (
            "Failed to refresh YouTube OAuth token: {}\n"
            "Possible causes:\n"
            "- refresh token is expired or revoked\n"
            "- refresh token was issued for a different client_id\n"
            "- client_id / client_secret do not match the token\n"
            "Fix: re-generate a new token with offline access and update the GitHub Secrets.\n"
            "See README or run a local token generator to get a fresh token."
        ).format(repr(e))
        raise RuntimeError(msg)

    return build("youtube", "v3", credentials=creds, cache_discovery=False)


# ---------------------------------------------------------------- الفيديو
def ar(text):
    return get_display(arabic_reshaper.reshape(text))


def wrap_lines(draw, text, font, max_width):
    lines, current = [], ""
    for word in text.split():
        candidate = (current + " " + word).strip()
        if draw.textlength(ar(candidate), font=font) <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_centered(draw, lines, font, y, color, gap=30):
    for line in lines:
        shaped = ar(line)
        w = draw.textlength(shaped, font=font)
        draw.text(((WIDTH - w) / 2, y), shaped, font=font, fill=color)
        y += font.size + gap
    return y


def make_frame(quote):
    if os.path.exists(BACKGROUND_IMAGE):
        img = Image.open(BACKGROUND_IMAGE).convert("RGB").resize((WIDTH, HEIGHT))
    else:
        img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_main = ImageFont.truetype(FONT_PATH, 84)
    font_src = ImageFont.truetype(FONT_PATH, 52)

    lines = wrap_lines(draw, quote["text"], font_main, WIDTH - 200)
    block_h = len(lines) * (font_main.size + 30)
    y = (HEIGHT - block_h) // 2 - 60
    y = draw_centered(draw, lines, font_main, y, TEXT_COLOR)
    draw_centered(draw, [quote["source"]], font_src, y + 40, SOURCE_COLOR)
    return np.array(img)


def build_video(quote, out_path="short.mp4"):
    audio_path = "voice.mp3"
    print("1/3 توليد الصوت ...")
    gTTS(text=quote["text"], lang="ar").save(audio_path)

    print("2/3 تركيب الفيديو ...")
    audio = AudioFileClip(audio_path)
    clip = (
        ImageClip(make_frame(quote))
        .set_duration(audio.duration + 1.0)
        .set_audio(audio)
    )
    clip.write_videofile(
        out_path, fps=24, codec="libx264", audio_codec="aac", logger=None
    )
    return out_path


# ---------------------------------------------------------------- الرفع
def upload(youtube, video_path, quote):
    title = f"{quote['text']} #Shorts"[:100]
    body = {
        "snippet": {
            "title": title,
            "description": f"{quote['text']}\n{quote['source']}\n\n#Shorts #قرآن #إسلاميات",
            "tags": ["Shorts", "قرآن", "إسلاميات"],
            "categoryId": "22",
        },
        "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False},
    }
    media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)
    request = youtube.videos().insert(
        part="snippet,status", body=body, media_body=media
    )
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"   رفع: {int(status.progress() * 100)}%")
    print("نجح الرفع. https://youtube.com/shorts/" + response["id"])


# ---------------------------------------------------------------- التشغيل
def main():
    print("bot started")
    quote = QUOTES[datetime.date.today().toordinal() % len(QUOTES)]
    print("النص:", quote["text"])

    # تحقق من المصادقة أولاً لتجنّب بناء الفيديو إذا كانت المصادقة ستفشل
    print("التحقق من المصادقة ...")
    youtube = get_authenticated_service()

    video_path = build_video(quote)
    print("3/3 رفع الفيديو ...")
    upload(youtube, video_path, quote)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR:", repr(e))
        sys.exit(1)
