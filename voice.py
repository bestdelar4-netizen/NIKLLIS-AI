"""
NIKLLIS Voice
"""

import pyttsx3


class Voice:

    def __init__(self):

        self.engine = pyttsx3.init()

        self.engine.setProperty("rate", 170)
        self.engine.setProperty("volume", 1.0)

    def speak(self, text):

        print(f"NIKLLIS: {text}")

        self.engine.say(text)

        self.engine.runAndWait()