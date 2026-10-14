import os, random, json
from PIL import Image, ImageDraw, ImageFont
import subprocess

IDEAS = [
    {"title": "القطوس كي يسمع كسكسي تم", "text": "لما ماما تقول كسكسي تم\nالقطوس: يجي يجري", "emoji": "😹"},
    {"title": "القطوس يناقش في سعر الزيت", "text": "الزيت ب 15 دينار؟\nيا رسول الله!", "emoji": "😂"},
    {"title": "طريقة الهريسة بسرعة", "text": "شوية هريسة + برشا ضحك\nوصفة القطوس", "emoji": "🌶️"},
]

def create_video():
    idea = random.choice(IDEAS)
    W, H = 1080, 1920
    bg = random.choice([(255,230,180), (180,255,200), (200,220,255)])
    img = Image.new('RGB', (W, H), bg)
    draw = ImageDraw.Draw(img)
    try:
        font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 65)
        font_med = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
    except:
        font_big = ImageFont.load_default()
        font_med = ImageFont.load_default()
    draw.text((W//2, 300), "كافيه ضحك تونسي", font=font_big, fill=(0,0,0), anchor="mm")
    draw.text((W//2, 450), idea["emoji"]*3, font=font_big, fill=(0,0,0), anchor="mm")
    draw.text((W//2, 650), idea["title"], font=font_big, fill=(180,0,0), anchor="mm")
    y = 900
    for line in idea["text"].split("\n"):
        draw.text((W//2, y), line, font=font_med, fill=(0,0,0), anchor="mm")
        y += 90
    draw.text((W//2, 1250), "بالشاشية", font=font_big, fill=(0,0,0), anchor="mm")
    img.save("frame.jpg")
    cmd = ["ffmpeg", "-y", "-loop", "1", "-i", "frame.jpg", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "15", "-vf", "scale=1080:1920", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "short.mp4"]
    subprocess.run(cmd, check=True)
    with open("video_info.json","w",encoding="utf-8") as f:
        json.dump({"title": idea["title"]+" #shorts", "description": f"{idea['text']}\n\nضحك تونسي", "tags": ["تونس","كوميديا","قطوس","shorts"]}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    create_video()
