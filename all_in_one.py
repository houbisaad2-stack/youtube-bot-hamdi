print("🤖 Bot Hamdi Starting...")
from PIL import Image, ImageDraw
import subprocess, os
W, H = 1280, 720
img = Image.new('RGB', (W, H), (255, 50, 50))
draw = ImageDraw.Draw(img)
draw.text((100, 300), "YouTube Bot Hamdi - Test Video", fill=(255,255,255))
img.save("frame.png")
print("✅ frame.png created")
cmd = ["ffmpeg", "-y", "-loop", "1", "-i", "frame.png", "-t", "5", "-pix_fmt", "yuv420p", "short.mp4"]
subprocess.run(cmd)
print(f"✅ short.mp4 created: {os.path.getsize('short.mp4')} bytes")
print("🎉 SUCCESS - Run is GREEN!")
