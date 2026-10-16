import os
import random
from gtts import gTTS
from moviepy.editor import ColorClip, AudioFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

# 1. قائمة النكات والاسكتشات التونسية المضحكة بالدارجة
TUNISIAN_JOKES = [
    "واحد ماشي يلوج على الخدمة، قالو المسؤول: اش تعرف تعمل؟ قالو: نعرف ننبر ونشجع من بعيد! قالو: مقبول طول مدير عام!",
    "واحد تونسي مشى يخطب، بو البنية قالو: وليدي البنت ما تعرفش تطيب! قالو التونسي: موش مشكل، توا نتعلموا مع بعضنا نطيبو ماكلة الحوت!",
    "الطفل التونسي كي يبدا يقرا: الأم تحلف عليه بالمصحف، والأب يهدد بالصباط، وفي الآخر ينجح بـ 10 سيدي عبيّس!",
    "واحد تونسي مشى للبحر في شتاء، سألوه علاش؟ قالهم: نلوج على الحوت المريض باش نداويه!",
    "قالك تونسي دخل للستاغ قالهم: فاتورتي غالية برشا! قالولو: أيا مبروك سيدي، ربحت معانا زوز بولات ضوء بلاش!"
]

def generate_joke():
    return random.choice(TUNISIAN_JOKES)

def create_audio(text, output_path="joke.mp3"):
    tts = gTTS(text=text, lang='ar', slow=False)
    tts.save(output_path)
    print(f"تم إنشاء الصوت بنجاح: {output_path}")
    return output_path

def create_auto_video(audio_path, output_video_path="final_video.mp4"):
    print("جاري إنشاء الفيديو تلقائياً بواسطة MoviePy...")
    
    # تحميل الصوت لمعرفة المدة الزمانية
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration + 1.0  # إضافة ثانية إضافية
    
    # إنشاء خلفية ملونة قياس Shorts (1080x1920)
    bg_color = random.choice([(20, 20, 40), (40, 10, 30), (10, 40, 30), (30, 30, 60)])
    video = ColorClip(size=(1080, 1920), color=bg_color, duration=duration)
    
    # إدماج الصوت في الفيديو
    video = video.set_audio(audio_clip)
    
    # حفظ الفيديو بصيغة mp4
    video.write_videofile(output_video_path, fps=24, codec='libx264', audio_codec='aac')
    print(f"🎉 تم إنشاء الفيديو بنجاح: {output_video_path}")
    return output_video_path

def upload_to_youtube(video_path, title):
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        print("خطأ: بيانات الاعتماد الخاصة بيوتيوب غير مكتملة في Secrets.")
        return

    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret
    )

    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": title[:90] + " #shorts #تونس #ضحك",
            "description": "فيديو كوميدي تونسي مضحك بالدارجة التونسية! اشترك في القناة للمزيد من الضحك.",
            "tags": ["تونس", "ضحك", "كوميديا", "Shorts", "تونسية"],
            "categoryId": "23"  # Comedy
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    response = request.execute()
    print(f"🚀 تم رفع الفيديو بنجاح إلى يوتيوب! الرابط: https://youtu.be/{response['id']}")

if __name__ == "__main__":
    print("--- بداية تشغيل البوت الكوميدي التونسي الآلي ---")
    joke_text = generate_joke()
    print(f"النكتة المحددة: {joke_text}")
    
    # 1. تحويل النص لصوت
    audio_file = create_audio(joke_text)
    
    # 2. إنشاء فيديو خلفية تلقائياً ودمج الصوت
    final_video = create_auto_video(audio_file)
    
    # 3. الرفع التلقائي ليوتيوب
    upload_to_youtube(final_video, joke_text)
