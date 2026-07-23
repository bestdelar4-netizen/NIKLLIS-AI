"""
NIKLLIS-AI - Interactive Web Assistant
"""

import json
import os
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)


class NikllisCore:

    def __init__(self):
        self.reminders_file = "reminders.json"
        self.load_reminders()

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

    def speak(self, text):
        safe_text = text.replace("'", "").replace('"', "")
        os.system(f"termux-tts-speak -l ar '{safe_text}' &")

    def process(self, cmd):
        cmd = cmd.lower().strip()

        if "اتصل" in cmd or "رن" in cmd:
            name = (
                cmd.replace("اتصل بـ", "")
                .replace("اتصل", "")
                .replace("رن على", "")
                .replace("رن", "")
                .strip()
            )
            self.speak(f"جاري الاتصال بـ {name}")
            os.system(f"termux-telephony-call '{name}'")
            return f"📞 جاري الاتصال بـ: {name}"

        elif "دواء" in cmd or "علاج" in cmd or "درس" in cmd or "سجل" in cmd:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            entry = {"detail": cmd, "created_at": now}
            self.reminders.append(entry)
            self.save_reminders()
            self.speak("تم تسجيل الميعاد بنجاح")
            return f"✅ تم حفظ التذكير: {cmd}"

        elif "مواعيدي" in cmd or "جدولي" in cmd or "تذكيراتي" in cmd:
            if not self.reminders:
                msg = "لا توجد مواعيد مسجلة حالياً."
            else:
                msg = f"لديك {len(self.reminders)} مواعيد مسجلة."
            self.speak(msg)
            return msg

        else:
            self.speak("استلمت أمرك وجاري معالجته")
            return f"🤖 استلمت الأمر: '{cmd}'"


core = NikllisCore()


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NIKLLIS-AI Assistant</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #fff; text-align: center; padding: 20px; }
            .card { background: #1e293b; border-radius: 20px; padding: 25px; margin: auto; max-width: 400px; box-shadow: 0 10px 25px rgba(0,0,0,0.6); border: 1px solid #334155; }
            .robot { width: 160px; height: 160px; margin: 15px auto; display: block; filter: drop-shadow(0 0 10px #38bdf888); }
            input { width: 80%; padding: 12px; border-radius: 10px; border: 1px solid #475569; background: #0f172a; color: white; font-size: 15px; margin-bottom: 12px; text-align: center; outline: none; }
            button { background: #38bdf8; color: #0f172a; border: none; padding: 12px 25px; border-radius: 10px; font-size: 16px; cursor: pointer; font-weight: bold; width: 85%; }
            button:active { background: #0284c7; }
            #status { margin-top: 18px; color: #38bdf8; font-weight: bold; font-size: 15px; min-height: 24px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2 style="color: #38bdf8; margin-bottom: 5px;">🤖 NIKLLIS-AI</h2>
            <p style="color: #94a3b8; font-size: 14px;">المساعد الشخصي الذكي</p>
            
            <svg class="robot" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
              <circle cx="100" cy="100" r="90" fill="#0f172a" stroke="#38bdf8" stroke-width="4"/>
              <!-- Antennas -->
              <line x1="100" y1="35" x2="100" y2="15" stroke="#38bdf8" stroke-width="6" stroke-linecap="round"/>
              <circle cx="100" cy="12" r="8" fill="#f43f5e"/>
              <!-- Ears -->
              <rect x="25" y="75" width="15" height="30" rx="5" fill="#38bdf8"/>
              <rect x="160" y="75" width="15" height="30" rx="5" fill="#38bdf8"/>
              <!-- Head -->
              <rect x="35" y="35" width="130" height="110" rx="25" fill="#1e293b" stroke="#38bdf8" stroke-width="4"/>
              <!-- Eyes Screen -->
              <rect x="50" y="55" width="100" height="45" rx="15" fill="#0f172a"/>
              <!-- Eyes -->
              <circle cx="75" cy="77" r="12" fill="#38bdf8"/>
              <circle cx="125" cy="77" r="12" fill="#38bdf8"/>
              <circle cx="78" cy="74" r="4" fill="#fff"/>
              <circle cx="128" cy="74" r="4" fill="#fff"/>
              <!-- Mouth / Cheeks -->
              <circle cx="60" cy="118" r="6" fill="#f43f5e" opacity="0.6"/>
              <circle cx="140" cy="118" r="6" fill="#f43f5e" opacity="0.6"/>
              <path d="M 80 115 Q 100 130 120 115" stroke="#38bdf8" stroke-width="5" stroke-linecap="round" fill="none"/>
            </svg>
            
            <div>
                <input type="text" id="cmdInput" placeholder="اكتب أمرك هنا (مثلاً: اتصل بـ احمد)">
                <button onclick="sendCommand()">🚀 إرسال الأمر</button>
            </div>
            
            <div id="status">جاهز للاستماع...</div>
        </div>

        <script>
            function sendCommand() {
                const input = document.getElementById('cmdInput');
                const val = input.value.trim();
                if(!val) return;
                
                document.getElementById('status').innerText = '⏳ جاري المعالجة...';
                
                fetch('/process?cmd=' + encodeURIComponent(val))
                .then(res => res.json())
                .then(data => {
                    document.getElementById('status').innerText = data.reply;
                    input.value = '';
                });
            }
        </script>
    </body>
    </html>
    """


@app.route("/process")
def process():
    cmd = request.args.get("cmd", "")
    reply = core.process(cmd)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
