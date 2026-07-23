"""
NIKLLIS-AI - Voice & Task Assistant Prototype
"""

import json
import os
import time


class NikllisAssistant:

  def __init__(self):
    self.name = "NIKLLIS-AI"
    self.tasks = []
    print(f"🤖 {self.name} initialized...")

  def add_reminder(self, task_name, time_str):
    """إضافة تذكير (مثل: دواء، تمرين، درس)"""
    reminder = {"task": task_name, "time": time_str}
    self.tasks.append(reminder)
    print(f"✅ تم تسجيل التذكير: {task_name} في موعد {time_str}")

  def make_call(self, contact_name):
    """تنفيذ إيماءة الاتصال برقم"""
    print(f"📞 جارٍ طلب الاتصال بـ: {contact_name}...")

  def process_command(self, command):
    """تحليل الأوامر الصوتية أو النصية"""
    cmd = command.lower().strip()

    if "اتصل" in cmd or "رن" in cmd:
      name = cmd.replace("اتصل بـ", "").replace("رن على", "").strip()
      self.make_call(name)

    elif "سجل" in cmd or "تذكير" in cmd:
      # مثال بسيط: سجل دواء الساعة 8
      self.add_reminder(task_name=cmd, time_str="الموعد المspecified")

    else:
      print(f"🤖 استلمت الأمر: '{command}'")


def main():
  assistant = NikllisAssistant()
  print("=" * 40)
  print("🤖 مرحباً بك في NIKLLIS-AI")
  print("=" * 40)

  while True:
    try:
      cmd = input("\n💬 ادخل أمرك (أو اكتب 'exit' للإنهاء): ")
      if cmd.strip().lower() == "exit":
        print("👋 إيقاف التشغيل...")
        break
      assistant.process_command(cmd)
    except KeyboardInterrupt:
      break


if __name__ == "__main__":
  main()
