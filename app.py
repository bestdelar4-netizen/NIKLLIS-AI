"""
NIKLLIS-AI - Siri-Class Always-On Voice Assistant
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

    def process(self, cmd):
        cmd = cmd.lower().strip()

        # تنظيف الكلمات التعريفية
        cmd = (
            cmd.replace("يا نيكليس", "")
            .replace("نيكليس", "")
            .replace("يا سيري", "")
            .replace("سيري", "")
            .strip()
        )

        if not cmd:
            return "مرحباً بك، أنا معك وسامعك طوال الوقت."

        if "اتصل" in cmd or "رن" in cmd:
            name = (
                cmd.replace("اتصل بـ", "")
                .replace("اتصل", "")
                .replace("رن على", "")
                .replace("رن", "")
                .strip()
            )
            os.system(f"termux-telephony-call '{name}'")
            return f"جاري الاتصال بـ {name}"

        elif "دواء" in cmd or "علاج" in cmd or "ذكرني" in cmd or "سجل" in cmd:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.reminders.append({"detail": cmd, "created_at": now})
            self.save_reminders()
            return f"تم تسجيل التذكير بنجاح: {cmd}"

        elif "مواعيدي" in cmd or "جدولي" in cmd:
            if not self.reminders:
                return "سجلك خالي تماماً من المواعيد."
            return f"لديك {len(self.reminders)} مهام ومواعيد مسجلة."

        elif "ازيك" in cmd or "من أنت" in cmd:
            return "أنا نظام NIKLLIS الذكي، معالجك الشخصي والمستمر معك دائماً."

        else:
            return f"سمعتك بتقول {cmd}، جارٍ معالجة الطلب."


core = NikllisCore()


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NIKLLIS-AI Always-On</title>
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, sans-serif; 
                background: radial-gradient(circle, #050b14 0%, #000000 100%); 
                color: #fff; text-align: center; margin: 0; padding: 0; 
                height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center;
            }
            .siri-container { position: relative; width: 140px; height: 140px; display: flex; justify-content: center; align-items: center; cursor: pointer; }
            .orb {
                width: 100px; height: 100px; border-radius: 50%;
                background: linear-gradient(135deg, #00c6ff 0%, #0072ff 50%, #7928ca 100%);
                box-shadow: 0 0 30px rgba(0, 198, 255, 0.6);
                animation: pulseOrb 2.5s infinite alternate ease-in-out;
            }
            .speaking { animation: speakPulse 0.5s infinite alternate !important; background: linear-gradient(135deg, #ff007f, #7928ca) !important; }
            @keyframes pulseOrb { 0% { transform: scale(0.95); } 100% { transform: scale(1.1); box-shadow: 0 0 50px #7928ca; } }
            @keyframes speakPulse { 0% { transform: scale(1); } 100% { transform: scale(1.25); box-shadow: 0 0 60px #ff007f; } }
            .status { margin-top: 20px; color: #a5b4fc; font-size: 14px; }
            .chat-box { width: 85%; max-width: 300px; height: 100px; overflow-y: auto; background: rgba(255,255,255,0.05); border-radius: 10px; padding: 10px; margin-top: 15px; font-size: 13px; text-align: right; }
        </style>
    </head>
    <body>
        <div class="siri-container" onclick="startAlwaysOn()">
            <div class="orb" id="orb"></div>
        </div>
        <div class="status" id="status">اضغط مرة واحدة لبدء الاتصال الدائم 🎙️</div>
        <div class="chat-box" id="chatBox"><div>المساعد جاهز...</div></div>

        <script>
            let recognition;
            let isSpeaking = false;

            function startAlwaysOn() {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!SpeechRecognition) return alert('المتصفح لا يدعم الصوت');

                recognition = new SpeechRecognition();
                recognition.lang = 'ar-SA';
                recognition.continuous = true;
                recognition.interimResults = false;

                recognition.onstart = function() {
                    document.getElementById('status').innerText = '🟢 متصل دائماً.. اتكلم في أي وقت';
                };

                recognition.onresult = function(event) {
                    if (isSpeaking) return; // عدم الاستماع أثناء حديث المساعد
                    const text = event.results[event.results.length - 1][0].transcript.trim();
                    processCmd(text);
                };

                recognition.onend = function() {
                    // إعادة التشغيل تلقائياً للبقاء متصلاً دائماً
                    setTimeout(() => { try { recognition.start(); } catch(e){} }, 300);
                };

                try { recognition.start(); } catch(e){}
            }

            function processCmd(text) {
                const box = document.getElementById('chatBox');
                box.innerHTML += '<div style="color:#38bdf8;">أنت: ' + text + '</div>';
                box.scrollTop = box.scrollHeight;

                fetch('/process?cmd=' + encodeURIComponent(text))
                .then(res => res.json())
                .then(data => {
                    box.innerHTML += '<div style="color:#c084fc;">نيكليس: ' + data.reply + '</div>';
                    box.scrollTop = box.scrollHeight;
                    speakResponse(data.reply);
                });
            }

            function speakResponse(text) {
                if ('speechSynthesis' in window) {
                    window.speechSynthesis.cancel();
                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.lang = 'ar-SA';
                    
                    utterance.onstart = function() {
                        isSpeaking = true;
                        document.getElementById('orb').className = 'orb speaking';
                    };
                    utterance.onend = function() {
                        isSpeaking = false;
                        document.getElementById('orb').className = 'orb';
                    };

                    window.speechSynthesis.speak(utterance);
                }
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
