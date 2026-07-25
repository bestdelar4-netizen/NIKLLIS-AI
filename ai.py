class AI:
    def __init__(self):
        self.name = "NIKLLIS AI"
        self.version = "1.0"

    def chat(self, text):
        text = text.lower().strip()

        if "اسمك" in text:
            return "اسمي NIKLLIS AI."

        elif "ازيك" in text or "عامل ايه" in text:
            return "أنا بخير، سعيد بالتحدث معك."

        elif "الوقت" in text:
            from datetime import datetime
            return "الوقت الآن " + datetime.now().strftime("%H:%M")

        elif "التاريخ" in text:
            from datetime import datetime
            return datetime.now().strftime("%Y-%m-%d")

        elif "شكرا" in text:
            return "العفو، أنا دائماً معك."

        elif "سلام" in text:
            return "إلى اللقاء."

        else:
            return None