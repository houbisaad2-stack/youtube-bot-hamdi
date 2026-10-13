print("🤣 Bot Hamdi - Nokat JDID 2025 Tounsi")
from PIL import Image, ImageDraw, ImageFont
import subprocess, os, json, random
from datetime import datetime

# 40 نكتة جديدة فريش 2024-2025 - تضحك بالرسمي
JOKES_NEW = [
    "تونسي حل ChatGPT\nقالو: خويا تنجم تعملي قهوة؟\nChatGPT: لا\nالتونسي: مالا شنوة فايدتك؟ 🤖☕",
    "الأم التونسية 2025:\nولدي نقص من التيك توك\nالولد: حاضر ماما *يحل انستا*\nالأم: نفس الحكاية! 📱😂",
    "تونسي طلب ياسير\nالشوفور: وين ماشي؟\nالتونسي: للدار\nالشوفور: وين الدار؟\nالتونسي: كان نعرف راني ما طلبتش ياسير! 🛵",
    "مرة تونسي الضو تقص عليه\nوهو يشحن في التليفون 1%\nقال: يا ربي كان تحبني\nرجع الضو 99% 🤣",
    "المعلم: علاش ما حفظتش؟\nالتلميذ: كنت نحفظ في ترند تيك توك\nالمعلم: وشنوة حفظت؟\nالتلميذ: حفظت الرقص! 💃",
    "تونسي مشى للسبيطار\nقالولو: عندك ستراس\nقال: لا عندي ويفي ضعيف\nنفس الحكاية! 📶😅",
    "مرة تونسي قال لمرتو:\nنحب نولي مشهور\nقاتلو: أغسل الماعون\nتوا تتشهر في الحومة! 🍽️😂",
    "القهواجي التونسي:\nقهوة بـ 2000\nوتبقى 3 سوايع على الويفي\nأرخص من البيرو! ☕",
    "تونسي سألوه: تخدم سبور؟\nقال: كل يوم\nقالولو: شنوة؟\nقال: نهز التليفون و نحطو\nنهز و نحط! 🏋️📱",
    "الأب التونسي كي يشوف فاتورة الانترنت:\n200 جيجا؟\nانت باش تحل شركة؟\nلا بابا نتفرج في ستوريات! 😭",
    "مرة تونسي حب يعمل دايت\nنهار الأول: سلطة\nنهار الثاني: شاف لبلابي\nنهار الثالث: الدايت هرب! 🥙😂",
    "تلميذ قال لصاحبو:\nالقراية صعيبة\nصاحبو: علاش؟\nقال: نقرا باش نخدم\nونخدم باش ننسى اللي قريتو! 🤯",
    "التونسية في المغازة:\n- هذا بقداش؟\n- 50 دينار\n- و هذا؟\n- 50 زادة\n- هات الزوز!\nما فهمتش المنطق! 🛍️",
    "تونسي عمل فيديو تيك توك\nجاب 2 vues\nواحدة هو\nو الثانية أمو باش تراقبو! 👀🤣",
    "مرة تونسي رقد بكري\nفاق مخلوع\nقال: شبيا فما حاجة؟\nلا والو رقدت بكري برك! 😴",
    "الكنترول في المترو:\nالتذكرة\nالتونسي: نسيتها في الدار\nالكنترول: و الدار وين؟\nالتونسي: نسيتها زادة! 🚇😂",
    "تونسي قال: باش نبطّل القهوة\nبعد 5 دقايق:\nزوز قهاوي و واحدة للطريق!\nالإرادة حديد! ☕💪",
    "الأم: نوض تقرا\nالولد: تو\nبعد ساعة: تو\nبعد ساعتين: تو\nكلمة تو عند التوانسة = never! ⏰",
    "مرة تونسي شاف سعر الطماطم 3 دينار\nقال: هذي طماطم ولا ذهب؟\nالخضار: ذهب أحمر!\nالتونسي: هات كيلو ذهب! 🍅💰",
    "تونسي في الخدمة:\nالمدير: اخدم\nالتونسي: نخدم\nالمدير: بالحق؟\nالتونسي: لا نتصور! 🤣",
    "الويفي في تونس:\nيخدم 10 دقايق\nويقص 10 سوايع\nويقولك: أنا موجود! 📶😭",
    "مرة تونسي حب يولي influencer\nصور فطورو\nاللبلابي\nجاب 10k likes!\nالسر في اللبلابي! 🔥",
    "التونسي كي يسمع غلاء المعيشة:\nما عادش ناكل برشا\nيضعف 100غ\nويقول: شفتو الرجيم؟ 😎",
    "أستاذ: وين الواجب؟\nتلميذ: الكلب كلاه\nأستاذ: ما عندكش كلب\nتلميذ: توة وليت عندي! 🐶😂",
    "تونسي طلب قهوة ليجار\nالقهواجي: نورمال ولا سبيسيال؟\nالتونسي: نورمال ب سوم سبيسيال!\nتونسي أصيل! ☕",
    "مرة تونسي ضاع في تونس\nسأل واحد: وين شارع الحبيب بورقيبة؟\nقالو: انت فيه!\nقال: مالا علاش ما لقيتوش! 🤣",
    "البنت التونسية:\nنحب واحد يفهمني\nالولد التونسي:\nأنا نفهم كان في الماكلة!\nالزواج ناجح! 🍕❤️",
    "تونسي شاف كرهبتو ما خدمتش\nضربها\nخدمت\nقال: التربية الحديثة!\nالضرب يجيب نتيجة! 🚗🔧",
    "الخدمة في تونس:\n8 سوايع خدمة\n7 سوايع قهوة\nوساعة نحكيو على الخدمة! 💼☕",
    "مرة تونسي قال: باش نرقد بكري اليوم\nالساعة 3 متاع الصباح:\nمازال بكري!\nتونسي حر! 🌙😂",
    "التونسي و السخانة 45°:\n- سخونة!\n- نشربو قهوة سخونة باش نبردو\nالمنطق التونسي! 🔥☕",
    "ولد صغير: بابا شنوة VPN؟\nباباه: حاجة كيما الباب\nتدخل بيها وين تحب\nبلا ما يشوفك حد! 😏",
    "تونسي في عرس:\nياكل\nيرقص\nيروح\nيقول: عرس باهي\nما نعرفش شكون عرس! 💃😂",
    "المعلمة: شنوة تحب تولي كي تكبر؟\nالتلميذ: نولي كبير\nونبطل نقرا!\nهدف واضح! 🎯",
    "مرة تونسي باع تليفونو\nباش يشري تليفون جديد\nالتليفون الجديد طلب mise à jour\nرجع للتليفون القديم! 📱",
    "التونسي كي يخلص:\nنهار فرحة\nنهارين حزن\nو 28 نهار حساب!\nالشهرية طايرة! 💸😅",
    "تونسية قالت لراجلها:\nهز الزبلة\nقال: تو\nقاتلو: تو قداش؟\nقال: تو متاع التوانسة! 🗑️",
    "مرة تونسي حب يتعلم انجليزية\nحفظ كلمة Hello\nمشى يحكي مع سائح\nقالو: هالو\nالسائح: هالو\nسكتوا الزوز! 🤝😂",
    "الكار في تونس:\nيجي معبي\nما ياقفش\nويقولك: الجاي خير!\nوالجاي كيفو! 🚌",
    "تونسي قال لصاحبو:\nعندي فكرة مشروع\nقالو: شنية؟\nقال: نبيع أفكار\nباش ما نخدمش! 💡🤣"
]

joke = random.choice(JOKES_NEW)

W, H = 720, 1280
colors = [(255, 59, 48), (0, 122, 255), (52, 199, 89), (255, 149, 0), (175, 82, 222), (255, 45, 85)]
bg = random.choice(colors)

img = Image.new('RGB', (W, H), bg)
draw = ImageDraw.Draw(img)
draw.rounded_rectangle([20, 300, W-20, 1000], radius=20, fill=(255,255,255), outline=(0,0,0), width=6)

lines = joke.split("\n")
y = 340
for line in lines:
    if len(line) > 28:
        words = line.split(" ")
        curr = ""
        for w in words:
            if len(curr + " " + w) < 26:
                curr += " " + w if curr else w
            else:
                bbox = draw.textbbox((0,0), curr)
                x = (W - (bbox[2]-bbox[0])) // 2
                draw.text((x, y), curr, fill=(0,0,0))
                y += 60
                curr = w
        if curr:
            bbox = draw.textbbox((0,0), curr)
            x = (W - (bbox[2]-bbox[0])) // 2
            draw.text((x, y), curr, fill=(0,0,0))
            y += 60
    else:
        bbox = draw.textbbox((0,0), line)
        x = (W - (bbox[2]-bbox[0])) // 2
        draw.text((x, y), line, fill=(0,0,0))
        y += 65
    y += 10

draw.text((W//2 - 120, 120), "نكت 2025 😂🔥", fill=(255,255,255), stroke_fill=(0,0,0), stroke_width=4)
draw.text((W//2 - 110, 200), "تضحك بالرسمي", fill=(255,255,255), stroke_fill=(0,0,0), stroke_width=3)
draw.text((W//2 - 100, 1050), "#نكت_تونسية", fill=(255,255,255), stroke_fill=(0,0,0), stroke_width=3)

img.save("frame.png")
cmd = ["ffmpeg", "-y", "-loop", "1", "-i", "frame.png", "-c:v", "libx264", "-t", "12", "-pix_fmt", "yuv420p", "-vf", "scale=720:1280", "short.mp4"]
subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

import json as js
with open("credentials.json") as f:
    data = js.load(f)
is_dummy = "dummy" in data["installed"]["refresh_token"].lower()

if is_dummy:
    print("🤣 DRY RUN - NOKTA JDIDA 2025")
    print(joke)
else:
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    creds_info = data["installed"]
    creds = Credentials(None, refresh_token=creds_info["refresh_token"], token_uri=creds_info["token_uri"], client_id=creds_info["client_id"], client_secret=creds_info["client_secret"], scopes=["https://www.googleapis.com/auth/youtube.upload"])
    creds.refresh(Request())
    youtube = build("youtube", "v3", credentials=creds)
    title = random.choice([f"نكتة تونسية جديدة 2025 تقتل 😂", f"تضحك ولا ما تضحكش؟ تونسية 100% 🤣", f"نكتة اليوم - كان تونسي تفهمها 🔥"])
    body = {"snippet": {"title": title, "description": f"{joke}\n\n#نكت_تونسية #تونس #ضحك #shorts", "tags": ["نكت تونسية جديدة", "ضحك 2025"], "categoryId": "23"}, "status": {"privacyStatus": "unlisted", "selfDeclaredMadeForKids": False}}
    media = MediaFileUpload("short.mp4", mimetype="video/mp4", resumable=True)
    resp = youtube.videos().insert(part="snippet,status", body=body, media_body=media).execute()
    print(f"🎉 UPLOADED! https://youtu.be/{resp['id']}")
