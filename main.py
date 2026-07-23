"""
NIKLLIS-AI - Voice Engine & Smart Assistant
"""

import json
from datetime import datetime
import os


class NikllisAssistant:

  def __init__(self):
    self.name = "NIKLLIS-AI"
    self.reminders_file = "reminders.json"
    self.load_reminders()
    self.speak("أهلاً بك! أنا نكليس جاهز لتلقي أوامرك")

  def speak(self, text):
    """تحويل النص إلى صوت في Termux أندرويد"""
    print(f"🤖 NIKLLIS: {text}")
    safe_text = text.replace("'", "").replace('"', "")
    os.system(f"termux-tts-speak -l ar '{safe_text}'")

  def load_reminders(self):
    if os.path.exists(self.reminders_file):
      try:
        with open(self.reminders_file, "r", encoding="utf-8") as f:
          self.reminders = json.load(f)
      except Exception:
        self.reminders = []
    else:
      self.reminders = []

  def save_reminders(self):
    with open(self.reminders_file, "w", encoding="utf-8") as f:
      json.dump(self.reminders, f, ensure_ascii=False, indent=4)

  def add_reminder(self, task_type, detail):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = {"type": task_type, "detail": detail, "created_at": now}
    self.reminders.append(entry)
    self.save_reminders()
    self.speak(f"تم تسجيل {task_type} بنجاح")

  def make_call(self, contact_name):
    self.speak(f"جاري الاتصال بـ {contact_name}")
    os.system(f"termux-telephony-call '{contact_name}'")

  def clean_name(self, text):
    """تنظيف الاسم من الكلمات المفتاحية"""
    for word in ["اتصل بـ", "اتصل", "رن على", "رن"]:
      text = text.replace(word, "")
    return text.strip()

  def process_command(self, command):
    cmd = command.lower().strip()

    if "اتصل" in cmd or "رن" in cmd:
      name = self.clean_name(cmd)
      self.make_call(name)

    elif "دواء" in cmd or "علاج" in cmd:
      self.add_reminder("ميعاد دواء", cmd)

    elif "تمرين" in cmd or "درس" in cmd or "سجل" in cmd:
      self.add_reminder("جدول زمني", cmd)

    elif "جدولي" in cmd or "تذكيراتي" in cmd or "مواعيدي" in cmd:
      if not self.reminders:
        self.speak("لا توجد مواعيد مسجلة في جدولك حالياً")
      else:
        self.speak(f"لديك {len(self.reminders)} مواعيد مسجلة")
        for i, item in enumerate(self.reminders, 1):
          print(f"{i}. [{item['type']}] {item['detail']}")

    else:
      self.speak("استلمت أمرك وجاري معالجته")


def main():
  assistant = NikllisAssistant()

  while True:
    try:
      cmd = input("\n🎙️ اكتب أو قول أمرك (أو اكتب 'exit' للإنهاء): ")
      if cmd.strip().lower() == "exit":
        assistant.speak("إلى اللقاء")
        break
      if cmd.strip():
        assistant.process_command(cmd)
    except KeyboardInterrupt:
      break


if __name__ == "__main__":
  main()

  def add_reminder(self, task_type, detail):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = {"type": task_type, "detail": detail, "created_at": now}
    self.reminders.append(entry)
    self.save_reminders()
    self.speak(f"تم تسجيل {task_type} بنجاح")

  def make_call(self, contact_name):
    self.speak(f"جاري الاتصال بـ {contact_name}")
    os.system(f"termux-telephony-call '{contact_name}'")

  def process_command(self, command):
    cmd = command.lower().strip()

    if "اتصل" in cmd or "رن" in cmd:
      name = (
          cmd.replace("اتصل بـ", "")
          .replace("اتصل", "")
          .replace("رن على", "")
          .replace("رن", "")
          .strip()
      )
      self.make_call(name)

    elif "دواء" in cmd or "علاج" in cmd:
      self.add_reminder("ميعاد دواء", cmd)

    elif "تمرين" in cmd or "درس" in cmd or "سجل" in cmd:
      self.add_reminder("جدول زمني", cmd)

    elif "جدولي" in cmd or "تذكيراتي" in cmd or "مواعيدي" in cmd:
      if not self.reminders:
        self.speak("لا توجد مواعيد مسجلة في جدولك حالياً")
      else:
        self.speak(f"لديك {len(self.reminders)} مواعيد مسجلة")
        for i, item in enumerate(self.reminders, 1):
          print(f"{i}. [{item['type']}] {item['detail']}")

    else:
      self.speak("استلمت أمرك وجاري معالجته")


def main():
  assistant = NikllisAssistant()

  while True:
    try:
      cmd = input("\n🎙️ اكتب أو قول أمرك (أو اكتب 'exit' للإنهاء): ")
      if cmd.strip().lower() == "exit":
        assistant.speak("إلى اللقاء")
        break
      if cmd.strip():
        assistant.process_command(cmd)
    except KeyboardInterrupt:
      break


if __name__ == "__main__":
  main()
          .replace("رن", "")
          .strip()
      )
      self.make_call(name)

    elif "دواء" in cmd or "علاج" in cmd:
      self.add_reminder("ميعاد دواء", cmd)

    elif "تمرين" in cmd or "درس" in cmd or "سجل" in cmd:
      self.add_reminder("جدول زمني", cmd)

    elif "جدولي" in cmd or "تذكيراتي" in cmd or "مواعيدي" in cmd:
      if not self.reminders:
        self.speak("لا توجد مواعيد مسجلة في جدولك حالياً")
      else:
        self.speak(f"لديك {len(self.reminders)} مواعيد مسجلة")
        for i, item in enumerate(self.reminders, 1):
          print(f"{i}. [{item['type']}] {item['detail']}")

    else:
      self.speak("استلمت أمرك وجاري معالجته")


def main():
  assistant = NikllisAssistant()

  while True:
    try:
      cmd = input("\n🎙️ اكتب أو قول أمرك (أو اكتب 'exit' للإنهاء): ")
      if cmd.strip().lower() == "exit":
        assistant.speak("إلى اللقاء")
        break
      if cmd.strip():
        assistant.process_command(cmd)
    except KeyboardInterrupt:
      break


if __name__ == "__main__":
  main()
  def save_reminders(self):
    with open(self.reminders_file, "w", encoding="utf-8") as f:
      json.dump(self.reminders, f, ensure_ascii=False, indent=4)

  def add_reminder(self, task_type, detail):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = {"type": task_type, "detail": detail, "created_at": now}
    self.reminders.append(entry)
    self.save_reminders()
    self.speak(f"تم تسجيل {task_type} بنجاح")

  def make_call(self, contact_name):
    self.speak(f"جاري الاتصال بـ {contact_name}")
    os.system(f"termux-telephony-call '{contact_name}'")

  def process_command(self, command):
    cmd = command.lower().strip()

    if "اتصل" in cmd or "رن" in cmd:
      name = (
          cmd.replace("اتصل بـ", "")
          .replace("اتصل", "")
          .replace("رن على", "")
          .replace("رن", "")
          .strip()
      )
      self.make_call(name)

    elif "دواء" in cmd or "علاج" in cmd:
      self.add_reminder("ميعاد دواء", cmd)

    elif "تمرين" in cmd or "درس" in cmd or "سجل" in cmd:
      self.add_reminder("جدول زمني", cmd)

    elif "جدولي" in cmd or "تذكيراتي" in cmd or "مواعيدي" in cmd:
      if not self.reminders:
        self.speak("لا توجد مواعيد مسجلة في جدولك حالياً")
      else:
        self.speak(f"لديك {len(self.reminders)} مواعيد مسجلة")
        for i, item in enumerate(self.reminders, 1):
          print(f"{i}. [{item['type']}] {item['detail']}")

    else:
      self.speak("استلمت أمرك وجاري معالجته")


def main():
  assistant = NikllisAssistant()

  while True:
    try:
      cmd = input("\n🎙️ تتكلم أو اكتب أمرك (اكتب 'exit' للإنهاء): ")
      if cmd.strip().lower() == "exit":
        assistant.speak("إلى اللقاء")
        break
      if cmd.strip():
        assistant.process_command(cmd)
    except KeyboardInterrupt:
      break


if __name__ == "__main__":
  main()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = {"type": task_type, "detail": detail, "created_at": now}
    self.reminders.append(entry)
    self.save_reminders()
    print(f"✅ تم تسجيل {task_type}: '{detail}' بنجاح!")

  def make_call(self, contact_name):
    """تنفيذ الاتصال بالأسماء"""
    print(f"📞 جارٍ الاتصال بـ: {contact_name}...")
    # تنفيذ أمر الاتصال في أندرويد عبر Termux API
    os.system(f"termux-telephony-call '{contact_name}'")

  def process_command(self, command):
    """تحليل الأوامر الصوتية أو النصية"""
    cmd = command.lower().strip()

    # 1. الاتصال
    if "اتصل" in cmd or "رن" in cmd:
      name = (
          cmd.replace("اتصل بـ", "")
          .replace("اتصل", "")
          .replace("رن على", "")
          .replace("رن", "")
          .strip()
      )
      self.make_call(name)

    # 2. جدولة أدوية
    elif "دواء" in cmd or "علاج" in cmd:
      self.add_reminder("ميعاد دواء", cmd)

    # 3. جدولة تمارين أو دروس
    elif "تمرين" in cmd or "درس" in cmd or "سجل" in cmd:
      self.add_reminder("جدول زمني/تذكير", cmd)

    # 4. عرض التذكيرات
    elif "جدولي" in cmd or "تذكيراتي" in cmd or "مواعيدي" in cmd:
      print("\n📋 جدولك الحالي:")
      if not self.reminders:
        print("لا توجد مواعيد مسجلة حتى الآن.")
      for i, item in enumerate(self.reminders, 1):
        print(f"{i}. [{item['type']}] {item['detail']}")

    else:
      print(f"🤖 NIKLLIS-AI استلم الأمر: '{command}'")


def main():
  assistant = NikllisAssistant()
  print("=" * 45)
  print("🤖 مرحباً بك في مشروع NIKLLIS-AI")
  print("=" * 45)

  while True:
    try:
      cmd = input("\n💬 ادخل أمرك (أو اكتب 'exit' للإنهاء): ")
      if cmd.strip().lower() == "exit":
        print("👋 إيقاف التشغيل...")
        break
      if cmd.strip():
        assistant.process_command(cmd)
    except KeyboardInterrupt:
      print("\n👋 إيقاف التشغيل...")
      break


if __name__ == "__main__":
  main()
