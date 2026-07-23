"""
NIKLLIS-AI - Michelin Character Voice Assistant
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

        # تنظيف كلمات النداء
        cmd = (
            cmd.replace("يا ميشلان", "")
            .replace("ميشلان", "")
            .replace("يا نكليس", "")
            .replace("نكليس", "")
            .strip()
        )

        if not cmd:
            reply = "أهلاً بيك! أنا ميشلان معك وسامعك كويس، أؤمرني؟"
            self.speak("أهلاً بيك! أنا ميشلان معك وسامعك كويس")
            return reply

        if "اتصل" in cmd or "رن" in cmd:
            name = (
                cmd.replace("اتصل بـ", "")
                .replace("اتصل", "")
                .replace("رن على", "")
                .replace("رن", "")
                .strip()
            )
            reply = f"📞 من عيوني! جاري الاتصال بـ: {name}"
            self.speak(f"جاري الاتصال بـ {name}")
            os.system(f"termux-telephony-call '{name}'")
            return reply

        elif "دواء" in cmd or "علاج" in cmd or "درس" in cmd or "سجل" in cmd:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            entry = {"detail": cmd, "created_at": now}
            self.reminders.append(entry)
            self.save_reminders()
            reply = f"✅ ميشلان سجل لك التذكير ده: {cmd}"
            self.speak("تم تسجيل الميعاد بنجاح")
            return reply

        elif "مواعيدي" in cmd or "جدولي" in cmd or "تذكيراتي" in cmd:
            if not self.reminders:
                reply = "جدولك فاضي ونظيف يا غالي، مافيش أي مواعيد."
            else:
                reply = f"عندك {len(self.reminders)} مواعيد مسجلة."
            self.speak(reply)
            return reply

        elif "ازيك" in cmd or "عامل ايه" in cmd or "اخبارك" in cmd:
            reply = "أنا زي الفل وجاهز لأي خدمة! أنت أخبارك إيه يا بطل؟"
            self.speak(reply)
            return reply

        else:
            reply = f"ميشلان سمعك بتقول: '{cmd}'.. قولي أعمل إيه فيها؟"
            self.speak("سمعتك، أساعدك إزاي؟")
            return reply


core = NikllisCore()


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NIKLLIS-AI - Michelin Assistant</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0b132b; color: #fff; text-align: center; padding: 10px; margin: 0; }
            .card { background: #1c2541; border-radius: 20px; padding: 20px; margin: auto; max-width: 400px; box-shadow: 0 10px 25px rgba(0,0,0,0.6); border: 2px solid #3a506b; }
            .michelin-avatar { width: 140px; height: 140px; margin: 10px auto; display: block; filter: drop-shadow(0 0 12px #ffffffaa); }
            .chat-box { height: 200px; overflow-y: auto; background: #0b132b; border-radius: 12px; padding: 10px; margin-bottom: 12px; text-align: right; border: 1px solid #3a506b; display: flex; flex-direction: column; gap: 8px; }
            .msg { padding: 8px 12px; border-radius: 10px; max-width: 80%; font-size: 14px; line-height: 1.4; }
            .user-msg { background: #6fffe9; color: #0b132b; align-self: flex-start; font-weight: bold; }
            .ai-msg { background: #3a506b; color: #ffffff; align-self: flex-end; }
            .status-btn { background: #ffc233; color: #0b132b; font-weight: bold; padding: 10px 15px; border-radius: 20px; border: none; font-size: 13px; cursor: pointer; width: 100%; margin-bottom: 10px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2 style="color: #6fffe9; margin: 0;">🏎️ NIKLLIS - ميشلان</h2>
            <button id="startBtn" class="status-btn" onclick="activateMic()">🔴 اضغط هنا لتفعيل الاستماع المباشر</button>
            
            <!-- تصميم شخصية ميشلان (Bibendum) -->
            <svg class="michelin-avatar" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
              <!-- Background Circle Glow -->
              <circle cx="100" cy="100" r="90" fill="#1c2541" stroke="#6fffe9" stroke-width="4"/>
              
              <!-- Body Rolls (Michelin Tires Body) -->
              <ellipse cx="100" cy="165" rx="55" ry="18" fill="#f8fafc" stroke="#cbd5e1" stroke-width="3"/>
              <ellipse cx="100" cy="142" rx="48" ry="16" fill="#ffffff" stroke="#cbd5e1" stroke-width="3"/>
              <ellipse cx="100" cy="120" rx="40" ry="14" fill="#f8fafc" stroke="#cbd5e1" stroke-width="3"/>
              
              <!-- Michelin Sash (الحزام الأزرق الشهير) -->
              <path d="M 65 110 Q 100 135 135 110" fill="none" stroke="#0284c7" stroke-width="12"/>
              
              <!-- Neck Roll -->
              <ellipse cx="100" cy="98" rx="30" ry="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="3"/>
              
              <!-- Head -->
              <circle cx="100" cy="72" r="28" fill="#ffffff" stroke="#cbd5e1" stroke-width="3"/>
              
              <!-- Eyes & Glasses (Michelin style) -->
              <circle cx="90" cy="68" r="5" fill="#0f172a"/>
              <circle cx="110" cy="68" r="5" fill="#0f172a"/>
              <circle cx="91" cy="66" r="1.5" fill="#ffffff"/>
              <circle cx="111" cy="66" r="1.5" fill="#ffffff"/>
              
              <!-- Smile -->
              <path d="M 88 80 Q 100 92 112 80" stroke="#0f172a" stroke-width="3" stroke-linecap="round" fill="none"/>
              <!-- Cheeks -->
              <circle cx="83" cy="78" r="4" fill="#f43f5e" opacity="0.4"/>
              <circle cx="117" cy="78" r="4" fill="#f43f5e" opacity="0.4"/>
            </svg>
            
            <div class="chat-box" id="chatBox">
                <div class="msg ai-msg">أهلاً بك! أنا صديقك ميشلان، فعل الاستماع ودردش معي أو نادِ علي برقم أو بـ "ميشلان"!</div>
            </div>
        </div>

        <script>
            let recognition;
            let active = false;

            function activateMic() {
                if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
                    alert('المتصفح لا يدعم التعرف الصوتي، استخدم متصفح Google Chrome');
                    return;
                }

                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                recognition = new SpeechRecognition();
                recognition.lang = 'ar-SA';
                recognition.continuous = true;
                recognition.interimResults = false;

                recognition.onstart = function() {
                    active = true;
                    document.getElementById('startBtn').innerText = '🎧 ميشلان يستمع إليك الآن... نادِ: ميشلان';
                    document.getElementById('startBtn').style.background = '#6fffe9';
                    document.getElementById('startBtn').style.color = '#0b132b';
                };

                recognition.onresult = function(event) {
                    const lastIndex = event.results.length - 1;
                    const text = event.results[lastIndex][0].transcript.trim();
                    console.log("المسموع:", text);
                    sendText(text);
                };

                recognition.onerror = function(e) {
                    restartMic();
                };

                recognition.onend = function() {
                    restartMic();
                };

                try { recognition.start(); } catch(e){}
            }

            function restartMic() {
                if(active) {
                    setTimeout(() => { try { recognition.start(); } catch(e){} }, 500);
                }
            }

            function appendMsg(text, sender) {
                const box = document.getElementById('chatBox');
                const div = document.createElement('div');
                div.className = 'msg ' + (sender === 'user' ? 'user-msg' : 'ai-msg');
                div.innerText = text;
                box.appendChild(div);
                box.scrollTop = box.scrollHeight;
            }

            function sendText(text) {
                appendMsg(text, 'user');
                
                fetch('/process?cmd=' + encodeURIComponent(text))
                .then(res => res.json())
                .then(data => {
                    appendMsg(data.reply, 'ai');
                    
                    if ('speechSynthesis' in window) {
                        window.speechSynthesis.cancel();
                        const utterance = new SpeechSynthesisUtterance(data.reply);
                        utterance.lang = 'ar-SA';
                        window.speechSynthesis.speak(utterance);
                    }
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
