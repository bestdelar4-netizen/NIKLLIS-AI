"""
NIKLLIS Reminder System
"""

import json
import os
from datetime import datetime


class Reminder:

    def __init__(self):

        self.file = "reminders.json"

        if os.path.exists(self.file):

            with open(self.file, "r", encoding="utf-8") as f:
                self.data = json.load(f)

        else:

            self.data = []

    def save(self):

        with open(self.file, "w", encoding="utf-8") as f:

            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def add(self, text):

        self.data.append({

            "text": text,

            "time": datetime.now().strftime("%Y-%m-%d %H:%M")

        })

        self.save()

        return "تم حفظ التذكير."

    def all(self):

        return self.data