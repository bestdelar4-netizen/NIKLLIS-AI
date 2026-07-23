from datetime import datetime
import threading
import time
import requests
import speech_recognition as sr

# ==========================================
# 1. إعدادات فيسبوك (Facebook API Configuration)
# ==========================================
FB_PAGE_ID = "YOUR_PAGE_ID"
FB_ACCESS_TOKEN = "YOUR_PAGE_ACCESS_TOKEN"


def schedule_facebook_post(message, delay_seconds=3600):
  """دالة لجدولة منشور على فيسبوك بعد مدة زمنية بالثواني"""
  url = f"https://graph.facebook.com/v18.0/{FB_PAGE_ID}/feed"
  target_time = int(time.time()) + delay_seconds

  payload = {
      "message": message,
      "published": False,
      "scheduled_publish_time": target_time,
      "access_token": FB_ACCESS_TOKEN,
  }

  try:
    response = requests.post(url, data=payload)
    result = response.json()
    if "id" in result:
      print(f"✅ تم جدولة البوست بنجاح! ID: {result['id']}")
    else:
      print(f"❌ خطأ من فيسبوك: {result}")
  except Exception as e:
    print(f"❌ فشل الاتصال بفيسبوك: {e}")


# ==========================================
# 2. محرك الاستماع للأوامر الصوتية
# ==========================================
def voice_assistant_loop():
  recognizer = sr.Recognizer()

  print("🤖 NIKLLIS-AI جاهز ويعمل على Termux...")
  print("🤖 حالة السكون (Idle Mode)... الروبوت يعمل في الخلفية!")

  while True:
    with sr.Microphone() as source:
      print("\n🎤 جارٍ الاستماع للأنشطة والأوامر...")
      recognizer.adjust_for_ambient_noise(source, duration=0.5)
      try:
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        command = recognizer.recognize_google(
            audio, language="ar-EG"
        ).lower()
        print(f"🗣️ الأسلوب/الأمر المسموع: {command}")

        # تحليل الأوامر الصوتية
        if "بوست" in command or "نزل" in command:
          print("🤖 جارٍ جدولة البوست على فيسبوك...")
          schedule_facebook_post(
              message=f"منشور تلقائي من NIKLLIS-AI: {command}",
              delay_seconds=600,  # بعد 10 دقائق كمثال
          )

        elif "رن على" in command or "اتصل" in command:
          name = command.replace("رن على", "").replace("اتصل", "").strip()
          print(f"📞 جارٍ طلب الاتصال بـ: {name}...")

      except (sr.WaitTimeoutError, sr.UnknownValueError):
        pass
      except Exception as e:
        print(f"⚠️ خطأ أثناء الاستماع: {e}")

    time.sleep(1)


if __name__ == "__main__":
  voice_assistant_loop()
