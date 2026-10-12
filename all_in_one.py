import os, time, random
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def authenticate():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        open("token.json","w").write(creds.to_json())
    return build("youtube","v3",credentials=creds)

def generate_video_ideas(niche="عام"):
    topics = ["قصة نجاح تونسية","وصفة تونسية","معلومة غريبة","تحدي 24 ساعة","نصائح للربح من الانترنت"]
    for i in range(10):
        print(f"{i+1}. {random.choice(topics)} | {niche}")

def growth_checklist():
    print("📈 خطة زيادة المتابعين:\n1. عنوان جذاب\n2. thumbnail اصفر\n3. رد على الكومنتارات\n4. Shorts كل يوم\n5. نشر 19:00-22:00")

def main():
    print("🚀 سوبر بوت يوتيوب - حميد")
    print("1. افكار فيديوهات\n2. خطة زيادة متابعين\n3. رفع فيديوهات")
    youtube = None
    while True:
        c = input("اختر: ").strip()
        if c=="1":
            niche=input("المجال؟ ") or "عام"
            generate_video_ideas(niche)
        elif c=="2":
            growth_checklist()
        elif c=="3":
            if not youtube: youtube=authenticate()
            print("حط فيديوهات في videos_to_upload/")
        elif c=="0": break

if __name__=="__main__": main()
