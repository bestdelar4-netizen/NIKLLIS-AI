"""
NIKLLIS-AI - Siri Experience + Interactive Floating Pet
"""
from ai import AI
import json
import os
from datetime import datetime
from flask import Flask, jsonify, request
from brain import Brain
from commands import Commands

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

        # تنظيف الكلمات
        cmd = (
            cmd.replace("يا نيكليس", "")
            .replace("نيكليس", "")
            .replace("يا سيري", "")
            .replace("سيري", "")
            .strip()
        )

        if not cmd:
            return "مرحباً بك، أنا معك وجاهز لأوامرك."

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
            return f"لديك {len(self.reminders)} مهام مسجلة."

        elif "العب" in cmd or "لعبة" in cmd:
            return "يا هلا! أنا مبسوط جداً وقاعد بلعب معاك ع الشاشة، امرني بطلب تاني أو ددش معايا."

        elif "ازيك" in cmd or "مين انت" in cmd:
            return "أنا مساعدك الذكي وكائنك المرافق، شبه سيري وأفضل كمان!"

        else:
            return f"سمعتك تقول: {cmd}، جارٍ التنفيذ."


core = NikllisCore()
brain = Brain()
commands = Commands()
ai = AI()

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Siri + Live Pet AI</title>
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, sans-serif; 
                background: #000; color: #fff; margin: 0; padding: 0; 
                height: 100vh; overflow: hidden; display: flex; flex-direction: column; justify-content: space-between; align-items: center;
            }
            
            /* منطقة الكائن الحي الصغير على الشاشة */
            .pet-container {
                margin-top: 15px;
                display: flex;
                flex-direction: column;
                align-items: center;
                cursor: pointer;
                animation: floatPet 3s ease-in-out infinite;
                z-index: 10;
            }
            @keyframes floatPet {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-8px); }
            }
            .pet-avatar {
                width: 60px; height: 60px;
                background: linear-gradient(135deg, #ff007f, #7928ca);
                border-radius: 50%;
                box-shadow: 0 0 15px rgba(255, 0, 127, 0.7);
                display: flex; justify-content: center; align-items: center;
                font-size: 28px;
                border: 2px solid #fff;
            }
            .pet-bubble {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(5px);
                padding: 4px 10px;
                border-radius: 12px;
                font-size: 11px;
                margin-top: 5px;
                color: #ffb4fc;
                border: 1px solid rgba(255,255,255,0.2);
            }

            /* شاشة سيري المركزية (Siri Orb) */
            .siri-center {
                display: flex; flex-direction: column; align-items: center; justify-content: center; flex: 1;
            }
            .siri-orb {
                width: 110px; height: 110px; border-radius: 50%;
                background: conic-gradient(from 0deg, #3b82f6, #8b5cf6, #ec4899, #3b82f6);
                animation: rotateOrb 4s linear infinite, pulseSiri 2s ease-in-out infinite alternate;
                box-shadow: 0 0 30px rgba(139, 92, 246, 0.5);
                cursor: pointer;
            }
            @keyframes rotateOrb { 0% { filter: hue-rotate(0deg); } 100% { filter: hue-rotate(360deg); } }
            @keyframes pulseSiri { 0% { transform: scale(0.95); } 100% { transform: scale(1.08); } }
            
            .speaking-orb {
                background: conic-gradient(from 0deg, #ef4444, #f59e0b, #10b981, #ef4444) !important;
                animation: rotateOrb 1.5s linear infinite, speakPulse 0.5s ease-in-out infinite alternate !important;
            }
            @keyframes speakPulse { 0% { transform: scale(1); } 100% { transform: scale(1.2); } }

            .status-text { margin-top: 15px; font-size: 13px; color: #94a3b8; letter-spacing: 0.5px; }

            /* صندوق محادثة سفلي مصغر */
            .chat-bar {
                width: 90%; max-width: 320px; height: 70px; overflow-y: auto;
                background: rgba(255,255,255,0.04); border-top: 1px solid rgba(255,255,255,0.1);
                padding: 8px; font-size: 11px; text-align: right; margin-bottom: 10px; border-radius: 10px;
            }
        </style>
    </head>
    <body onclick="initVoiceSystem()">

        <!-- الكائن الصغير المرافق على الشاشة -->
        <div class="pet-container" onclick="feedPet(event)">
            <div class="pet-avatar" id="petEmoji">👾</div>
            <div class="pet-bubble" id="petMsg">اضغط عليّ للعب!</div>
        </div>

        <!-- شكل سيري الأساسي -->
        <div class="siri-center">
            <div class="siri-orb" id="siriOrb"></div>
            <div class="status-text" id="statusText">انقر في أي مكان للبدء...</div>
        </div>

        <div class="chat-bar" id="chatBox">
            <div>النظام جاهز...</div>
        </div>

        <script>
            let recognition;
            let isStarted = false;
            let isSpeaking = false;

            function initVoiceSystem() {
                if (isStarted) return;
                isStarted = true;
                
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!SpeechRecognition) return alert('المتصفح لا يدعم التعرف الصوتي');

                recognition = new SpeechRecognition();
                recognition.lang = 'ar-SA';
                recognition.continuous = true;
                recognition.interimResults = false;

                recognition.onstart = function() {
                    document.getElementById('statusText').innerText = 'سيري تستمع إليك الآن...';
                };

                recognition.onresult = function(event) {
                    if (isSpeaking) return;
                    const text = event.results[event.results.length - 1][0].transcript.trim();
                    handleCommand(text);
                };

                recognition.onend = function() {
                    setTimeout(() => { try { recognition.start(); } catch(e){} }, 300);
                };

                try { 
                    recognition.start(); 
                    document.getElementById('statusText').innerText = 'متصل وجاهز للأوامر';
                } catch(e){}
            }

            function feedPet(e) {
                e.stopPropagation();
                const emojis = ['👾', '🐱', '🤖', '🦊', '⚡'];
                const randomEmoji = emojis[Math.floor(Math.random() * emojis.length)];
                document.getElementById('petEmoji').innerText = randomEmoji;
                
                const phrases = ['شكراً ع الاكل!', 'يلا بينا نلعب!', 'أنا معك يا بطل!', 'منور يا غالي!'];
                const randomPhrase = phrases[Math.floor(Math.random() * phrases.length)];
                document.getElementById('petMsg').innerText = randomPhrase;
                
                if ('speechSynthesis' in window) {
                    const utter = new SpeechSynthesisUtterance(randomPhrase);
                    utter.lang = 'ar-SA';
                    window.speechSynthesis.speak(utter);
                }
            }

            function handleCommand(text) {
                const box = document.getElementById('chatBox');
                box.innerHTML += '<div style="color:#38bdf8;">أنت: ' + text + '</div>';
                box.scrollTop = box.scrollHeight;

                fetch('/process?cmd=' + encodeURIComponent(text))
                .then(res => res.json())
                .then(data => {
                    box.innerHTML += '<div style="color:#c084fc;">سيري: ' + data.reply + '</div>';
                    box.scrollTop = box.scrollHeight;
                    speakSiri(data.reply);
                });
            }

            function speakSiri(text) {
                if ('speechSynthesis' in window) {
                    window.speechSynthesis.cancel();
                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.lang = 'ar-SA';

                    utterance.onstart = function() {
                        isSpeaking = true;
                        document.getElementById('siriOrb').className = 'siri-orb speaking-orb';
                        document.getElementById('statusText').innerText = 'تتحدث...';
                    };
                    utterance.onend = function() {
                        isSpeaking = false;
                        document.getElementById('siriOrb').className = 'siri-orb';
                        document.getElementById('statusText').innerText = 'تستمع...';
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

    # تنظيف كلمة النداء
    cmd = (
        cmd.replace("يا نيكليس", "")
        .replace("نيكليس", "")
        .replace("يا سيري", "")
        .replace("سيري", "")
        .strip()
    )

    # تنفيذ أوامر النظام
    result = commands.execute(cmd)

    if result:

        if result["action"] == "call":
            os.system(f'termux-telephony-call "{result["target"]}"')

        return jsonify(result)

    # التفكير والرد
    reply = brain.think(cmd)

if reply is None:
    reply = ai.reply(cmd)
    if reply is None:
        reply = core.process(cmd)

    return jsonify({
        "reply": reply,
        "action": ""
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
