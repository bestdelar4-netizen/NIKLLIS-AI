class Brain:

    def __init__(self):
        self.username = "سيف"

    def think(self, text):

        text = text.lower()

        if "ازيك" in text:
            return "أنا بخير يا سيف."

        if "اسمك" in text:
            return "اسمي NIKLLIS."

        if "بحبك" in text:
            return "وأنا سعيد إني أساعدك يا سيف."

        return None