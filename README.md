# youtube-bot-hamdi
بوت يوتيوب يدير القناة - auto upload و auto reply

## إعداد المصادقة الآمنة

لا تضع أي مفتاح Google أو client_secret داخل ملفات المشروع أو داخل GitHub.

1. انسخ الملف `.env.example` إلى `.env`
2. املأ القيم الحقيقية من Google Cloud Console أو من OAuth flow
3. لا ترفع `.env` أو `token.json` أو أي ملف OAuth إلى GitHub

مثال:

```bash
cp .env.example .env
```

ثم عدّل الملف:

```env
YOUTUBE_CLIENT_ID=...
YOUTUBE_CLIENT_SECRET=...
YOUTUBE_REFRESH_TOKEN=...
```

أو استخدم `YOUTUBE_TOKEN_JSON` إذا كان لديك JSON كامل للـ OAuth Token.

## ملاحظات الأمان
- الملف `.env` مستثنى تلقائيًا بواسطة `.gitignore`
- لا تضع `client_secret` داخل `bot.py` أو `auth.py`
- إذا كنت تستخدم GitHub Actions أو Secrets، خزّن القيم داخل Repository Secrets فقط

## التشغيل

```bash
pip install -r requirements.txt
python bot.py
```
