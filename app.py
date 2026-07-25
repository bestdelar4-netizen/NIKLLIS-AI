"""
NIKLLIS-AI - Siri Experience + Interactive Floating Pet
"""
from ai import AI
import json
import os
from datetime import datetime
from flask import Flask, jsonify, request, render_template
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
    return render_template("index.html")


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
        reply = ai.chat(cmd)

    if reply is None:
        reply = core.process(cmd)

    return jsonify({
        "reply": reply,
        "action": ""
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)