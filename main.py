from datetime import datetime
import time
import requests

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
# 2. المساعد الذكي NIKLLIS-AI
# ==========================================
def assistant_loop():
  print("=" * 40)
  print("🤖 NIKLLIS-AI جاهز ويعمل بنجاح على Termux!")
  print("💡 يمكنك استخدام الإملاء الصوتي من الكيبورد!")
  print("=" * 40)

  while True:
    try:
      command = input("\n💬 اكتب أمرك أو استخدم إملاء المايك (اكتب 'خروج' للإنهاء): ").lower()

      if command.strip() == "":
        continue

      if "خروج" in command or "exit" in command:
        print("👋 تم إيقاف NIKLLIS-AI.")
        break

      # تحليل الأوامر
      if "بوست" in command or "نزل" in command or "جدولة" in command:
        print("🤖 جارٍ جدولة البوست على فيسبوك...")
        schedule_facebook_post(
            message=f"منشور تلقائي من NIKLLIS-AI: {command}",
            delay_seconds=600,  # بعد 10 دقائق
        )

      elif "رن" in command or "اتصل" in command:
        name = command.replace("رن على", "").replace("اتصل", "").strip()
        print(f"📞 جارٍ تنفيذ طلب الاتصال بـ: {name}...")

      else:
        print(f"🤖 استلمت الأمر: '{command}' .. جارٍ المعالجة.")

    except KeyboardInterrupt:
      print("\n👋 تم الخروج.")
      break


if __name__ == "__main__":
  assistant_loop()
