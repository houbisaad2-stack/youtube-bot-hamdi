import os, json, random, subprocess
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from PIL import Image, ImageDraw, ImageFont

print("Starting bot...")

# 1. Load credentials (workflow يكتبهم client.json و token.json)
CLIENT_FILE = "client.json"
TOKEN_FILE = "token.json"

# يدعم الزوز طرق: من secrets مباشرة ولا من فايلات
if os.getenv("YOUTUBE_CLIENT_JSON"):
    Path(CLIENT_FILE).write_text(os.getenv("YOUTUBE_CLIENT_JSON"))
if os.getenv("YOUTUBE_TOKEN_JSON"):
    Path(TOKEN_FILE).write_text(os.getenv("YOUTUBE_TOKEN_JSON"))

with open(CLIENT_FILE) as f:
    client_info = json.load(f)
with open(TOKEN_FILE) as f:
    token_info = json.load(f)

creds = Credentials.from_authorized_user_info(token_info, ["https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.upload"])

if creds.expired and creds.refresh_token:
    print("Refreshing token...")
    creds.refresh(Request())
    # save new token
    Path(TOKEN_FILE).write_text(creds.to_json())

youtube = build("youtube", "v3", credentials=creds)
print("YouTube auth OK")

# 2. Generate video 720x1280 - 7 seconds
W, H = 720, 1280
quotes = [
    "Did you know? Your brain uses 20% of your energy!",
    "Fact: Octopuses have 3 hearts!",
    "Motivation: Small steps every day = Big results!",
    "Fact: Honey never spoils!",
    "Mindset: Done is better than perfect."
]
text = random.choice(quotes)

img = Image.new("RGB", (W, H), (15, 15, 35))
draw = ImageDraw.Draw(img)
# حاول تكتب النص في الوسط
try:
    # نحاولو نلقاو font
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)
except:
    font = ImageFont.load_default()

# تقسيم النص
def wrap(t, max_chars=22):
    words = t.split()
    lines, cur = [], ""
    for w in words:
        if len(cur + " " + w) <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

lines = wrap(text)
y = H//2 - len(lines)*35
for line in lines:
    bbox = draw.textbbox((0,0), line, font=font)
    w = bbox[2]-bbox[0]
    draw.text(((W-w)//2, y), line, fill=(255,255,255), font=font)
    y += 70

img.save("frame.jpg")
print(f"Image created: {text}")

# حول الصورة لفيديو بـ ffmpeg (موجود في GitHub runner)
video_path = "video.mp4"
subprocess.run([
    "ffmpeg", "-y",
    "-loop", "1", "-i", "frame.jpg",
    "-c:v", "libx264", "-t", "7",
    "-pix_fmt", "yuv420p",
    "-vf", "scale=720:1280",
    video_path
], check=True)

print("Video generated")

# 3. Upload to YouTube as Short
title = text[:90] + " #shorts"
body = {
    "snippet": {
        "title": title,
        "description": f"{text}\n\n#shorts #facts #motivation #auto",
        "tags": ["shorts", "facts", "motivation", "auto"],
        "categoryId": "27"
    },
    "status": {
        "privacyStatus": "public",
        "selfDeclaredMadeForKids": False
    }
}

media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)
request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
response = request.execute()
print(f"Uploaded! Video ID: {response['id']} - https://youtu.be/{response['id']}")
