"""
NIKLLIS Commands
"""

import os


class Commands:

    def execute(self, text):

        text = text.lower().strip()

        # الاتصال
        if "رن" in text or "اتصل" in text:
            name = (
                text.replace("رن على", "")
                .replace("رن", "")
                .replace("اتصل على", "")
                .replace("اتصل", "")
                .strip()
            )

            return {
                "action": "call",
                "target": name,
                "reply": f"حاضر يا سيف، جاري الاتصال بـ {name}"
            }

        # واتساب
        if "واتساب" in text:
            return {
                "action": "whatsapp",
                "reply": "جاري فتح واتساب."
            }

        # يوتيوب
        if "يوتيوب" in text:
            return {
                "action": "youtube",
                "reply": "جاري فتح يوتيوب."
            }

        # الكاميرا
        if "الكاميرا" in text:
            return {
                "action": "camera",
                "reply": "جاري فتح الكاميرا."
            }

        # الكشاف
        if "الكشاف" in text:
            return {
                "action": "flash",
                "reply": "جاري تشغيل الكشاف."
            }

        return None