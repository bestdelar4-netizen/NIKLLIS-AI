from datetime import datetime
import threading
import time
import requests
import speech_recognition as sr
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QLabel, QWidget

# ==========================================
# 1. إعدادات فيسبوك (بياناتك الخاصة)
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
# 2. واجهة الروبوت المتحرك (PyQt5)
# ==========================================
class FloatingRobot(QWidget):

  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    self.setWindowFlags(
        Qt.FramelessWindowHint
        | Qt.WindowStaysOnTopHint
        | Qt.SubWindow
        | Qt.Tool
    )
    self.setAttribute(Qt.WA_TranslucentBackground, True)
    self.setGeometry(100, 100, 150, 150)

    self.label = QLabel(self)
    self.movie = QMovie("robot_idle.gif")  # ضع صورة GIF هنا
    self.label.setMovie(self.movie)
    self.movie.start()

    self.x_dir = 2
    self.timer = QTimer(self)
    self.timer.timeout.connect(self.move_robot)
    self.timer.start(50)

  def move_robot(self):
    current_pos = self.pos()
    new_x = current_pos.x() + self.x_dir
    screen_width = QApplication.primaryScreen().size().width()

    if new_x > screen_width - 150 or new_x < 0:
      self.x_dir *= -1

    self.move(new_x, current_pos.y())


# ==========================================
# 3. محرك الاستماع للأوامر الصوتية
# ==========================================
def voice_assistant_loop():
  recognizer = sr.Recognizer()

  while True:
    with sr.Microphone() as source:
      print("\n🎤 الروبوت يستمع الآن...")
      recognizer.adjust_for_ambient_noise(source, duration=0.5)
      try:
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        command = recognizer.recognize_google(
            audio, language="ar-EG"
        ).lower()
        print(f"🗣️ سمعت: {command}")

        # تحليل الأمر
        if "بوست" in command or "نزل" in command:
          print("🤖 جارٍ جدولة البوست على فيسبوك...")
          # مثال: جدولة بوست تجريبي بعد 10 دقائق
          schedule_facebook_post(
              message=f"منشور تلقائي من NIKLLIS-AI: {command}",
              delay_seconds=600,
          )

        elif "رن على" in command or "اتصل" in command:
          name = command.replace("رن على", "").replace("اتصل", "").strip()
          print(f"📞 جارٍ الاتصال بـ {name}...")

      except sr.WaitTimeoutError:
        pass
      except sr.UnknownValueError:
        pass
      except Exception as e:
        print(f"⚠️ خطأ: {e}")

    time.sleep(1)


# ==========================================
# 4. تشغيل التطبيق بالكامل
# ==========================================
if __name__ == "__main__":
  import sys

  # تشغيل الاستماع في Thread مستقل لعدم تجميد واجهة الروبوت
  voice_thread = threading.Thread(target=voice_assistant_loop, daemon=True)
  voice_thread.start()

  # تشغيل واجهة الروبوت المتحرك
  app = QApplication(sys.argv)
  pet = FloatingRobot()
  pet.show()
  sys.exit(app.exec_())

