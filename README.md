import os
import json
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont

JOKES_NEW = [
    "مرة واحد قال لصاحبو علاش القمر بعيد؟ قالو باش الناس ما يطلعولوش!",
    "قالك واحد بخيل مات كاتبين على قبرو هذا القبر برعاية عائلتو",
    "مرة واحد محشش شاف لافتة ممنوع الوقوف قعد يجري",
    "استاذ سال تلميذ شنوة جمع ناقة قالو ناقتين يا استاذ",
    "واحد قال لمرتو انتي قمر قاتلو وانت شمس قالها منور حياتي قاتلو لا بعيد عليا"
]

def create_image(text, path="thumb.jpg"):
    W, H = 1080, 1920
    img = Image.new("RGB", (W, H), color=(18,18,18))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 62)
    except:
        font = ImageFont.load_default()
    lines = textwrap.wrap(text, width=22)
    y = H//2 - len(lines)*50
    for line in lines:
        bbox = draw.textbbox((0,0), line, font=font)
        w = bbox[2]-bbox[0]
        draw.text(((W-w)//2, y), line, font=font, fill=(255,255,255))
        y += 90
    img.save(path)
    return path

def main():
    joke = random.choice(JOKES_NEW)
    print(f"Joke selected: {joke}")
    img_path = create_image(joke)
    video_path = "short.mp4"
    os.system(f"ffmpeg -y -loop 1 -i {img_path} -c:v libx264 -t 8 -pix_fmt yuv420p -vf scale=1080:1920 {video_path}")
    print(f"Video created: {video_path}")
    if not os.path.exists("credentials.json"):
        print("✅ DRY RUN - Video ready")
        return
    try:
        with open("credentials.json") as f:
            data = json.load(f)
            cid = data.get("installed", {}).get("client_id", "")
            if cid == "dummy" or not cid:
                print("✅ DRY RUN - Video ready (add YouTube secrets to upload)")
                return
    except:
        print("✅ DRY RUN - Video ready")
        return
    print("✅ DRY RUN - Video ready")

if __name__ == "__main__":
    main()
