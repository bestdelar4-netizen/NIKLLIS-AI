"""
NIKLLIS-AI - Hands-Free Always Listening Assistant
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

        # تنظيف كلمة النداء لو اتنطقت مع الأمر
        cmd = (
            cmd.replace("يا نكليس", "")
            .replace("نكليس", "")
            .replace("يا نيكليس", "")
            .replace("نيكليس", "")
            .strip()
        )

        if "اتصل" in cmd or "رن" in cmd:
            name = (
                cmd.replace("اتصل بـ", "")
                .replace("اتصل", "")
                .replace("رن على", "")
                .replace("رن", "")
                .strip()
            )
            reply = f"📞 جاري الاتصال بـ: {name}"
            self.speak(f"جاري الاتصال بـ {name}")
            os.system(f"termux-telephony-call '{name}'")
            return reply

        elif "دواء" in cmd or "علاج" in cmd or "درس" in cmd or "سجل" in cmd:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            entry = {"detail": cmd, "created_at": now}
            self.reminders.append(entry)
            self.save_reminders()
            reply = f"✅ سجلت التذكير ده: {cmd}"
            self.speak("تم تسجيل الميعاد بنجاح")
            return reply

        elif "مواعيدي" in cmd or "جدولي" in cmd or "تذكيراتي" in cmd:
            if not self.reminders:
                reply = "مافيش أي مواعيد مسجلة حالياً."
            else:
                reply = f"عندك {len(self.reminders)} مواعيد مسجلة يا غالي."
            self.speak(reply)
            return reply

        elif "ازيك" in cmd or "عامل ايه" in cmd or "اخبارك" in cmd:
            reply = "أنا سامعك وشغال معاك تمام! تؤمرني بإيه؟"
            self.speak(reply)
            return reply

        elif "صباح" in cmd:
            reply = "صباح الفل والسرور!"
            self.speak(reply)
            return reply

        elif "مساء" in cmd:
            reply = "مساء السعادة والورد!"
            self.speak(reply)
            return reply

        else:
            reply = f"نعم! أومرني، أعمل إيه بخصوص '{cmd}'؟"
            self.speak("نعم سامعك، تؤمر بإيه؟")
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
        <title>NIKLLIS-AI Always Listening</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #fff; text-align: center; padding: 10px; margin: 0; }
            .card { background: #1e293b; border-radius: 20px; padding: 20px; margin: auto; max-width: 400px; box-shadow: 0 10px 25px rgba(0,0,0,0.6); border: 1px solid #334155; }
            .robot { width: 130px; height: 130px; margin: 10px auto; display: block; filter: drop-shadow(0 0 10px #38bdf888); transition: 0.3s; }
            .active-pulse { animation: pulse 1s infinite; filter: drop-shadow(0 0 25px #38bdf8) !important; }
            @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.08); } 100% { transform: scale(1); } }
            
            .chat-box { height: 220px; overflow-y: auto; background: #0f172a; border-radius: 12px; padding: 10px; margin-bottom: 12px; text-align: right; border: 1px solid #334155; display: flex; flex-direction: column; gap: 8px; }
            .msg { padding: 8px 12px; border-radius: 10px; max-width: 80%; font-size: 14px; line-height: 1.4; }
            .user-msg { background: #38bdf8; color: #0f172a; align-self: flex-start; font-weight: bold; }
            .ai-msg { background: #334155; color: #f8fafc; align-self: flex-end; }
            
            .status-tag { display: inline-block; background: #10b981; color: #0f172a; font-weight: bold; padding: 5px 12px; border-radius: 20px; font-size: 12px; margin-bottom: 10px; }
        </style>
    </head>
    <body onclick="startContinuousListening()">
        <div class="card">
            <h2 style="color: #38bdf8; margin: 0;">🤖 NIKLLIS-AI</h2>
            <div id="statusTag" class="status-tag">🎧 المساعد يستمع الآن... نادِ عليه: "نكليس"</div>
            
            <svg id="robotSvg" class="robot active-pulse" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
              <circle cx="100" cy="100" r="90" fill="#0f172a" stroke="#38bdf8" stroke-width="4"/>
              <line x1="100" y1="35" x2="100" y2="15" stroke="#38bdf8" stroke-width="6" stroke-linecap="round"/>
              <circle cx="100" cy="12" r="8" fill="#f43f5e"/>
              <rect x="25" y="75" width="15" height="30" rx="5" fill="#38bdf8"/>
              <rect x="160" y="75" width="15" height="30" rx="5" fill="#38bdf8"/>
              <rect x="35" y="35" width="130" height="110" rx="25" fill="#1e293b" stroke="#38bdf8" stroke-width="4"/>
              <rect x="50" y="55" width="100" height="45" rx="15" fill="#0f172a"/>
              <circle cx="75" cy="77" r="12" fill="#38bdf8"/>
              <circle cx="125" cy="77" r="12" fill="#38bdf8"/>
              <circle cx="78" cy="74" r="4" fill="#fff"/>
              <circle cx="128" cy="74" r="4" fill="#fff"/>
              <circle cx="60" cy="118" r="6" fill="#f43f5e" opacity="0.6"/>
              <circle cx="140" cy="118" r="6" fill="#f43f5e" opacity="0.6"/>
              <path d="M 80 115 Q 100 130 120 115" stroke="#38bdf8" stroke-width="5" stroke-linecap="round" fill="none"/>
            </svg>
            
            <div class="chat-box" id="chatBox">
                <div class="msg ai-msg">أنا سامعك دايماً! أول ما تنادي وتقول "نكليس" أو "يا نكليس" هرد عليك مباشرةً.</div>
            </div>
        </div>

        <script>
            let recognition;
            const WAKE_WORDS = ["نكليس", "نيكليس", "يا نكليس", "يا نيكليس"];

            function initSpeech() {
                if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    recognition = new SpeechRecognition();
                    recognition.lang = 'ar-AR';
                    recognition.continuous = true; // استماع مستمر بدون توقف
                    recognition.interimResults = false;

                    recognition.onresult = function(event) {
                        const lastIndex = event.results.length - 1;
                        const text = event.results[lastIndex][0].transcript.trim();
                        console.log("الكلمة المسموعة:", text);

                        // التحقق هل تم المناداة بالكلمة السحرية أو توجيه أمر مباشر
                        const hasWakeWord = WAKE_WORDS.some(word => text.includes(word));

                        if (hasWakeWord || text.length > 3) {
                            sendText(text);
                        }
                    };

                    recognition.onend = function() {
                        // إعادة التشغيل تلقائياً لو اتقفل من المتصفح لضمان الاستماع المستمر
                        recognition.start();
                    };

                    recognition.onerror = function(event) {
                        setTimeout(() => { recognition.start(); }, 1000);
                    };

                    recognition.start();
                } else {
                    document.getElementById('statusTag').innerText = '⚠️ المتصفح لا يدعم الاستماع الصوتي';
                }
            }

            function startContinuousListening() {
                if(recognition) {
                    try { recognition.start(); } catch(e) {}
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
                        window.speechSynthesis.cancel(); // إيقاف أي صوت سابق
                        const utterance = new SpeechSynthesisUtterance(data.reply);
                        utterance.lang = 'ar-SA';
                        window.speechSynthesis.speak(utterance);
                    }
                });
            }

            // تشغيل الاستماع فور تحميل الصفحة
            window.onload = initSpeech;
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
