"""
NIKLLIS AI
"""

import random


class AI:

    def __init__(self):
        self.owner = "سيف"

        self.happy = [
            "تحت أمرك يا سيف.",
            "أنا معك.",
            "ماذا تريد؟",
            "يسعدني مساعدتك."
        ]

        self.sad = [
            "واضح إنك متضايق، هل أقدر أساعد؟",
            "إن شاء الله الأمور تتحسن.",
            "أنا معك."
        ]

    def reply(self, text):

        text = text.lower()

        if "بحبك" in text:
            return "وأنا سعيد أني معك يا سيف."

        if "زعلان" in text:
            return random.choice(self.sad)

        return random.choice(self.happy)