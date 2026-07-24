"""
NIKLLIS AI Brain
"""

from datetime import datetime


class Brain:

    def __init__(self):
        self.name = "NIKLLIS"
        self.owner = "سيف"

    def think(self, text):

        text = text.lower().strip()

        if not text:
            return "أنا معك يا سيف."

        # التحية
        if "السلام" in text or "اهلا" in text or "ازيك" in text:
            return f"أهلاً يا {self.owner}."

        # الاسم
        if "اسمك" in text:
            return "اسمي NIKLLIS."

        # الوقت
        if "الوقت" in text or "الساعة" in text:
            return datetime.now().strftime("الوقت الآن %H:%M")

        # التاريخ
        if "التاريخ" in text:
            return datetime.now().strftime("%Y-%m-%d")

        # الحب 😄
        if "بحبك" in text:
            return "وأنا سعيد أني معاك يا سيف."

        # من أنت
        if "مين انت" in text:
            return "أنا مساعدك الذكي NIKLLIS."

        # وداع
        if "مع السلامه" in text:
            return "أشوفك قريب يا سيف."

        return None