"""
NIKLLIS-AI - Desktop/Android Assistant GUI
"""

import os
import tkinter as tk
from tkinter import messagebox


class NikllisApp:

  def __init__(self, root):
    self.root = root
    self.root.title("NIKLLIS-AI Assistant")
    self.root.geometry("350x500")
    self.root.configure(bg="#1e1e2e")

    # Title Label
    self.title_label = tk.Label(
        root,
        text="🤖 NIKLLIS-AI",
        font=("Helvetica", 20, "bold"),
        fg="#cba6f7",
        bg="#1e1e2e",
    )
    self.title_label.pack(pady=20)

    # Status Label
    self.status_label = tk.Label(
        root,
        text="👋 أنا نكليس جاهز لتلقي أوامرك",
        font=("Helvetica", 12),
        fg="#bac2de",
        bg="#1e1e2e",
    )
    self.status_label.pack(pady=10)

    # Speak / Mic Button
    self.mic_btn = tk.Button(
        root,
        text="🎙️ التحدث / تنفيذ أمر",
        font=("Helvetica", 14, "bold"),
        bg="#89b4fa",
        fg="#11111b",
        padx=10,
        pady=5,
        command=self.run_command,
    )
    self.mic_btn.pack(pady=20)

    # Output Box
    self.output_box = tk.Text(
        root,
        height=10,
        width=35,
        bg="#313244",
        fg="#a6adc8",
        font=("Consolas", 10),
    )
    self.output_box.pack(pady=10)

  def run_command(self):
    self.status_label.config(text="🎤 جاري الاستماع والاستجابة...")
    self.output_box.insert(tk.END, "🤖 NIKLLIS: تم الضغط على المايك!\n")
    # استدعاء الصوت
    os.system("termux-tts-speak -l ar 'أنا أستمع إليك الآن'")


if __name__ == "__main__":
  root = tk.Tk()
  app = NikllisApp(root)
  root.mainloop()
