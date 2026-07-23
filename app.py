"""
NIKLLIS-AI - Web GUI Interface for Mobile
"""

import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)


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
            body { font-family: sans-serif; background-color: #121212; color: #fff; text-align: center; padding: 20px; }
            .card { background: #1e1e1e; border-radius: 15px; padding: 20px; margin: auto; max-width: 400px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
            .robot { width: 180px; height: auto; border-radius: 10px; margin: 15px 0; }
            button { background: #007bff; color: white; border: none; padding: 12px 25px; border-radius: 25px; font-size: 16px; cursor: pointer; }
            button:active { background: #0056b3; }
            #status { margin-top: 15px; color: #00ffcc; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>🤖 NIKLLIS-AI</h2>
            <p>المساعد الشخصي الذكي</p>
            <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHp1eHN3Ymc5aTh3NDV3eTYycTFiaXpjdnd4czM4YzI1eHgzYXpmeSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKSjRrfIPjeiVyM/giphy.gif" class="robot" alt="Robot Mascot">
            <div>
                <button onclick="speak()">🎙️ اضغط للتحدث</button>
            </div>
            <div id="status">جاهز للاستماع...</div>
        </div>

        <script>
            function speak() {
                document.getElementById('status').innerText = '🎤 جاري التفاعل واستلام الأمر...';
                fetch('/run_mic')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('status').innerText = data.message;
                });
            }
        </script>
    </body>
    </html>
    """


@app.route("/run_mic")
def run_mic():
  os.system("termux-tts-speak -l ar 'أنا أستمع إليك الآن'")
  return jsonify({"message": "✅ تم تفعيل المساعد الصوتي!"})


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
