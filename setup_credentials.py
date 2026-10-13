import os, json, random, textwrap
from PIL import Image, ImageDraw, ImageFont

JOKES_NEW = [
    "مرة واحد قال لصاحبو علاش القمر بعيد؟ قالو باش الناس ما يطلعولوش!",
    "قالك واحد بخيل مات، كاتبين على قبرو: هذا القبر برعاية عائلتو!",
    "مرة واحد محشش شاف لافتة مكتوب عليها ممنوع الوقوف، قعد يجري!",
    "قالك استاذ سأل تلميذ: شنوة جمع كلمة ناقة؟ قالو: ناقتين يا استاذ!",
    "واحد قال لمرتو: انتي قمر! قاتلو: وانت شمس! قالها: قصدك منور حياتي؟ قاتلو: لا قصدي بعيد عليا!",
]

def create_image(text, path="thumb.jpg"):
    W, H = 1080, 1920
    img = Image.new("RGB", (W, H), color=(18,18,18))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 62)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 62)
        except:
            font = ImageFont.load_default()

    lines = textwrap.wrap(text, width=22)
    y = H//2 - len(lines)*50
    for line in lines:
        bbox = draw.textbbox((0,0), line, font=font)
        w = bbox[2]-bbox[0]
        draw.text(((W-w)//2, y), line, font=font, fill=(255,255,255), stroke_width=2, stroke_fill=(0,0,0))
        y += 90
    img.save(path)
    return path

def main():
    joke = random.choice(JOKES_NEW)
    print(f"Joke: {joke}")
    img_path = create_image(joke, "thumb.jpg")
    video_path = "short.mp4"
    cmd = f'ffmpeg -y -loop 1 -i {img_path} -c:v libx264 -t 8 -pix_fmt yuv420p -vf "scale=1080:1920" {video_path}'
    os.system(cmd)
    print(f"Video created: {video_path}")

    if not os.path.exists("credentials.json"):
        print("✅ DRY RUN - Video ready (no credentials.json)")
        return

    try:
        with open("credentials.json") as f:
            data = json.load(f)
            cid = data.get("installed", {}).get("client_id", "")
            if cid == "dummy" or not cid:
                print("✅ DRY RUN - Video ready (dummy credentials - add YouTube secrets to upload)")
                return
    except Exception as e:
        print(f"✅ DRY RUN - Video ready (creds error: {e})")
        return

    print("Trying upload... (real upload needs valid secrets)")
    # Upload logic here when secrets are added
    print("✅ DRY RUN - Video ready")

if __name__ == "__main__":
    main()
