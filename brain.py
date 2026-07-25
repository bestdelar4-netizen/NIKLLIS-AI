from datetime import datetime


class Brain:

    def __init__(self):
        self.owner = "سيف"

    def think(self, text):

        text = text.lower().strip()

        if not text:
            return "تحت أمرك يا سيف."

        if "ازيك" in text:
            return "أنا بخير يا سيف."

        if "اسمك" in text:
            return "أنا NIKLLIS."

        if "مين انت" in text:
            return "أنا مساعدك الشخصي."

        if "الوقت" in text:
            return datetime.now().strftime("%H:%M")

        if "التاريخ" in text:
            return datetime.now().strftime("%Y-%m-%d")

        if "بحبك" in text:
            return "وأنا سعيد أني معاك."

        return None