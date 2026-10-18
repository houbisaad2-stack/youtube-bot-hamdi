import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def get_youtube_service():
    # جلب البيانات من متغرات البيئة في غيتهاب
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        raise ValueError("بعض المتغيرات (CLIENT_ID / CLIENT_SECRET / YOUTUBE_TOKEN) مفقودة في GitHub Secrets!")

    # إنشاء الاعتمادات باستخدام YOUTUBE_TOKEN
    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )

    # تجديد الـ Access Token تلقائياً
    if not creds.valid:
        creds.refresh(Request())

    # بناء خدمة YouTube API
    return build("youtube", "v3", credentials=creds)

if __name__ == "__main__":
    try:
        youtube = get_youtube_service()
        print("✅ تم الاتصال بـ YouTube API وتحديث الرمز بنجاح!")
        # هنا يوضع كود الإنشاء والرفع الخاص بك
    except Exception as e:
        print(f"❌ حدث خطأ أثناء الاتصال: {e}")
