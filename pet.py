"""
NIKLLIS Pet System
"""

import random


class Pet:

    def __init__(self):
        self.state = "happy"
        self.energy = 100

    def idle(self):

        actions = [
            "ينظر إليك 👀",
            "يرمش 😊",
            "يتجول على الشاشة 🚶",
            "يجلس قليلاً 🪑",
            "يلعب 🎮",
        ]

        return random.choice(actions)

    def sleep(self):

        self.state = "sleep"

        return "😴 نيكليس نام."

    def wake(self):

        self.state = "happy"

        return "صباح الخير يا سيف ❤️"

    def play(self):

        self.state = "play"

        return "هيا نلعب 😄"

    def status(self):

        return {
            "state": self.state,
            "energy": self.energy
        }