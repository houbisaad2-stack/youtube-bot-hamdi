import os, json, random, subprocess
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from PIL import Image, ImageDraw, ImageFont
print("Starting bot...")
CLIENT_FILE="client.json";TOKEN_FILE="token.json"
if os.getenv("YOUTUBE_CLIENT_JSON"):
    Path(CLIENT_FILE).write_text(os.getenv("YOUTUBE_CLIENT_JSON"))
if os.getenv("YOUTUBE_TOKEN_JSON"):
    Path(TOKEN_FILE).write_text(os.getenv("YOUTUBE_TOKEN_JSON"))
with open(CLIENT_FILE) as f:
    client_info=json.load(f)
with open(TOKEN_FILE) as f:
    token_info=json.load(f)
creds=Credentials.from_authorized_user_info(token_info, ["https://www.googleapis.com/auth/youtube","https://www.googleapis.com/auth/youtube.upload"])
if creds.expired and creds.refresh_token:
    creds.refresh(Request());Path(TOKEN_FILE).write_text(creds.to_json())
youtube=build("youtube","v3",credentials=creds)
print("Auth OK")
W,H=720,1280
quotes=["Did you know? Your brain uses 20% of your energy!","Fact: Octopuses have 3 hearts!","Motivation: Small steps every day = Big results!","Fact: Honey never spoils!","Mindset: Done is better than perfect."]
text=random.choice(quotes)
img=Image.new("RGB",(W,H),(15,15,35));draw=ImageDraw.Draw(img)
try:
    font=ImageFont.truetype("DejaVuSans-Bold.ttf",48)
except:
    font=ImageFont.load_default()
def wrap(t,max_chars=22):
    words=t.split();lines,cur=[],"";
    for w in words:
        if len(cur+" "+w)<=max_chars:
            cur=(cur+" "+w).strip()
        else:
            lines.append(cur);cur=w
    if cur:
        lines.append(cur)
    return lines
lines=wrap(text);y=H//2-len(lines)*35
for line in lines:
    bbox=draw.textbbox((0,0),line,font=font);w=bbox[2]-bbox[0]
    draw.text(((W-w)//2,y),line,fill=(255,255,255),font=font);y+=70
img.save("frame.jpg")
subprocess.run(["ffmpeg","-y","-loop","1","-i","frame.jpg","-c:v","libx264","-t","7","-pix_fmt","yuv420p","-vf","scale=720:1280","video.mp4"],check=True)
title=text[:90]+" #shorts"
body={"snippet":{"title":title,"description":f"{text}\n\n#shorts #facts #auto","tags":["shorts"],"categoryId":"27"},"status":{"privacyStatus":"public","selfDeclaredMadeForKids":False}}
media=MediaFileUpload("video.mp4",mimetype="video/mp4",resumable=True)
resp=youtube.videos().insert(part="snippet,status",body=body,media_body=media).execute()
print(f"Uploaded: https://youtu.be/{resp['id']}")
