import os
import yt_dlp
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

# ------------------------------------
# 1. دالة جلب وتحميل الفيديو من الرابط
# ------------------------------------
def download_video(video_url, output_path='temp_video.mp4'):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': output_path,
        'quiet': True
    }
    
    print("⏳ جاري تحميل الفيديو...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    print("✅ تم تحميل الفيديو بنجاح!")
    return output_path

# ------------------------------------
# 2. دالة تسجيل الدخول ورفع الفيديو ليوتيوب
# ------------------------------------
def upload_to_youtube(video_file, title, description, tags=None, category_id="22"):
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    # يتطلب وجود ملف client_secrets.json في نفس المستودع لاحقاً
    flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
    credentials = flow.run_local_server(port=0)
    
    youtube = build('youtube', 'v3', credentials=credentials)
    
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags or [],
            'categoryId': category_id  # 22 تعبر عن الفئة العامة People & Blogs
        },
        'status': {
            'privacyStatus': 'private'  # يمكنك تغييرها إلى 'public' لنشرها علناً لاحقاً
        }
    }
    
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )
    
    print("⏳ جاري رفع الفيديو إلى القناة...")
    response = request.execute()
    print(f"🎉 تم الرفع بنجاح! معرّف الفيديو: {response.get('id')}")
    
    # حذف الملف المؤقت بعد الرفع للحفاظ على مساحة التخزين
    if os.path.exists(video_file):
        os.remove(video_file)

# ------------------------------------
# 3. تشغيل العمليتين معاً
# ------------------------------------
if __name__ == '__main__':
    target_url = "ضع_رابط_الفيديو_هنا"  # ضع رابط الفيديو المراد جلبه بين العلامتين
    
    # خطوة 1: التحميل
    downloaded_file = download_video(target_url)
    
    # خطوة 2: الرفع
    upload_to_youtube(
        video_file=downloaded_file,
        title="عنوان الفيديو تلقائي",
        description="تم رفع هذا الفيديو بواسطة البوت تلقائياً.",
        tags=["bot", "youtube", "python"]
    )
