"""
NIKLLIS Contacts
"""

import json
import os


class Contacts:

    def __init__(self):
        self.file = "contacts.json"

        if os.path.exists(self.file):
            with open(self.file, "r", encoding="utf-8") as f:
                self.contacts = json.load(f)
        else:
            self.contacts = {
                "محمد": "محمد",
                "احمد": "احمد",
                "ماما": "ماما",
                "بابا": "بابا"
            }

    def search(self, name):

        name = name.strip()

        for contact in self.contacts:
            if name in contact:
                return self.contacts[contact]

        return None