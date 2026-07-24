"""
NIKLLIS-AI - Ultimate Siri Competitor Assistant
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
            cmd.replace("يا نيكليس", "")
            .replace("نيكليس", "")
            .replace("يا سيري", "")
            .replace("سيري", "")
            .strip()
        )

        if not cmd:
            reply = "مرحباً بك، أنا نيكليس معك وجاهز لأوامرك."
            self.speak(reply)
            return reply

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

        elif "دواء" in cmd or "علاج" in cmd or "ذكرني" in cmd or "سجل" in cmd:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            entry = {"detail": cmd, "created_at": now}
            self.reminders.append(entry)
            self.save_reminders()
            reply = f"🛡️ تم الحفظ في الذاكرة بنجاح: {cmd}"
            self.speak("تم حفظ التذكير بنجاح")
            return reply

        elif "مواعيدي" in cmd or "جدولي" in cmd:
            if not self.reminders:
                reply = "سجلك نظيف، لا توجد مواعيد معلقة."
            else:
                reply = f"لديك {len(self.reminders)} مهام مسجلة."
            self.speak(reply)
            return reply

        elif "ازيك" in cmd or "من أنت" in cmd or "عرفني نفسك" in cmd:
            reply = "أنا نظام NIKLLIS الذكي، مساعدك الشخصي المتطور."
            self.speak(reply)
            return reply

        else:
            reply = f"معالجة الطلب: '{cmd}'.. جارٍ التنفيذ."
            self.speak("تتم المعالجة الآن")
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
        <title>NIKLLIS-AI - Neural Assistant</title>
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                background: radial-gradient(circle, #050b14 0%, #000000 100%); 
                color: #fff; text-align: center; margin: 0; padding: 0; 
                height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center;
            }
            .siri-container {
                position: relative; width: 150px; height: 150px; display: flex; justify-content: center; align-items: center; cursor: pointer;
            }
            .orb {
                width: 100px; height: 100px; border-radius: 50%;
                background: linear-gradient(135deg, #00c6ff 0%, #0072ff 50%, #7928ca 100%);
                box-shadow: 0 0 30px rgba(0, 198, 255, 0.6), inset 0 0 20px rgba(255, 255, 255, 0.4);
                animation: pulseOrb 3s infinite alternate ease-in-out;
                transition: 0.3s;
            }
            @keyframes pulseOrb {
                0% { transform: scale(0.95); box-shadow: 0 0 20px rgba(0, 198, 255, 0.4); }
                100% { transform: scale(1.1); box-shadow: 0 0 50px rgba(121, 40, 202, 0.8); }
            }
            .listening {
                background: linear-gradient(135deg, #ff007f 0%, #7928ca 50%, #00c6ff 100%) !important;
                animation: listenPulse 0.8s infinite alternate !important;
            }
            @keyframes listenPulse {
                0% { transform: scale(1); box-shadow: 0 0 40px #ff007f; }
                100% { transform: scale(1.25); box-shadow: 0 0 70px #00c6ff; }
            }
            .status-text { margin-top: 25px; font-size: 15px; letter-spacing: 1px; color: #a5b4fc; font-weight: 500; }
            .chat-box { 
                width: 85%; max-width: 320px; height: 90px; overflow-y: auto; 
                background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); 
                border-radius: 12px; padding: 10px; margin-top: 15px; font-size: 12px; text-align: right; 
                backdrop-filter: blur(10px);
            }
        </style>
    </head>
    <body>
        <div class="siri-container" onclick="toggleMic()">
            <div class="orb" id="orb"></div>
        </div>
        
        <div class="status-text" id="statusText">اضغط على كرة الطاقة للتحدث</div>
        
        <div class="chat-box" id="chatBox">
            <div>النظام جاهز للاستماع...</div>
        </div>

        <script>
            let recognition;
            let active = false;

            function toggleMic() {
                if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
                    alert('متصفحك لا يدعم التعرف الصوتي');
                    return;
                }

                if(!active) {
                    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    recognition = new SpeechRecognition();
                    recognition.lang = 'ar-SA';
                    recognition.continuous = true;
                    recognition.interimResults = false;

                    recognition.onstart = function() {
                        active = true;
                        document.getElementById('orb').className = 'orb listening';
                        document.getElementById('statusText').innerText = 'أنا أستمع إليك الآن...';
                    };

                    recognition.onresult = function(event) {
                        const lastIndex = event.results.length - 1;
                        const text = event.results[lastIndex][0].transcript.trim();
                        sendText(text);
                    };

                    recognition.onerror = function(e) { restartMic(); };
                    recognition.onend = function() { restartMic(); };

                    try { recognition.start(); } catch(e){}
                } else {
                    active = false;
                    if(recognition) recognition.stop();
                    document.getElementById('orb').className = 'orb';
                    document.getElementById('statusText').innerText = 'تم الإيقاف. اضغط للتفعيل';
                }
            }

            function restartMic() {
                if(active) {
                    setTimeout(() => { try { recognition.start(); } catch(e){} }, 300);
                }
            }

            function sendText(text) {
                const box = document.getElementById('chatBox');
                box.innerHTML += '<div style="color:#38bdf8; margin:3px 0;">أنت: ' + text + '</div>';
                box.scrollTop = box.scrollHeight;
                
                fetch('/process?cmd=' + encodeURIComponent(text))
                .then(res => res.json())
                .then(data => {
                    box.innerHTML += '<div style="color:#c084fc; margin:3px 0;">نيكليس: ' + data.reply + '</div>';
                    box.scrollTop = box.scrollHeight;
                    
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
