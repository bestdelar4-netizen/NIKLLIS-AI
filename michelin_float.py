"""
NIKLLIS-AI - Michelin Floating Widget
"""

import os
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget

# ضبط حجم النافذة لتكون صغيرة وعائمة
Window.size = (180, 220)
Window.borderless = True  # بدون شريط علوي
Window.top = 100
Window.left = 100


class MichelinAvatar(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.draw_michelin()

    def draw_michelin(self):
        self.canvas.clear()
        with self.canvas:
            # الخلفية
            Color(0.11, 0.15, 0.25, 0.9)
            Ellipse(pos=(10, 10), size=(160, 160))

            # جسم ميشلان
            Color(0.97, 0.98, 0.99, 1)
            Ellipse(pos=(45, 25), size=(90, 35))
            Ellipse(pos=(50, 50), size=(80, 30))
            Ellipse(pos=(55, 70), size=(70, 25))

            # الرأس
            Ellipse(pos=(65, 90), size=(50, 50))

            # العيون
            Color(0.06, 0.09, 0.16, 1)
            Ellipse(pos=(78, 115), size=(8, 8))
            Ellipse(pos=(94, 115), size=(8, 8))

            # الابتسامة
            Color(0.06, 0.09, 0.16, 1)
            Line(points=[80, 102, 90, 96, 100, 102], width=2)


class FloatingMichelinApp(App):

    def build(self):
        root = BoxLayout(orientation="vertical", padding=5, spacing=5)

        # رسم أشكال ميشلان
        self.avatar = MichelinAvatar(size_hint=(1, 0.7))
        root.add_widget(self.avatar)

        # زر التفاعل مع ميشلان
        self.status_lbl = Label(
            text="يا ميشلان!",
            font_size="13sp",
            bold=True,
            size_hint=(1, 0.15),
            color=(0.43, 1, 0.91, 1),
        )
        root.add_widget(self.status_lbl)

        btn = Button(
            text="🎙️ تكلم",
            size_hint=(1, 0.15),
            background_color=(0.22, 0.74, 0.97, 1),
        )
        btn.bind(on_press=self.on_mic_click)
        root.add_widget(btn)

        return root

    def on_mic_click(self, instance):
        self.status_lbl.text = "سامعك.. اتكلم!"
        # تشغيل الصوت لـ Termux
        os.system("termux-tts-speak -l ar 'نعم يا بطل، أنا ميشلان سامعك' &")


if __name__ == "__main__":
    FloatingMichelinApp().run()
