"""
NIKLLIS Commands
"""

import os


class Commands:

    def execute(self, text):

        text = text.lower().strip()

        # ===== الاتصال =====
        if "رن" in text or "اتصل" in text:

            name = (
                text.replace("رن على", "")
                .replace("رنلي على", "")
                .replace("اتصل على", "")
                .replace("اتصل", "")
                .replace("رن", "")
                .strip()
            )

            return {
                "action": "call",
                "target": name,
                "reply": f"حاضر يا سيف، جاري الاتصال بـ {name}"
            }

        # ===== واتساب =====
        if "واتساب" in text:
            return {
                "action": "whatsapp",
                "reply": "جاري فتح واتساب."
            }

        # ===== يوتيوب =====
        if "يوتيوب" in text:
            return {
                "action": "youtube",
                "reply": "جاري فتح يوتيوب."
            }

        # ===== الكاميرا =====
        if "الكاميرا" in text:
            return {
                "action": "camera",
                "reply": "جاري فتح الكاميرا."
            }

        # ===== الإعدادات =====
        if "الاعدادات" in text or "الإعدادات" in text:
            return {
                "action": "settings",
                "reply": "جاري فتح الإعدادات."
            }

        # ===== الكشاف =====
        if "الكشاف" in text:
            return {
                "action": "flash",
                "reply": "جاري تشغيل الكشاف."
            }

        return None