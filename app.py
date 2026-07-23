"""
NIKLLIS-AI - Android Floating Mascot & Voice App Interface
"""

import os
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


class NikllisApp(App):

  def build(self):
    self.title = "NIKLLIS-AI Assistant"

    # Layout رئيسي
    main_layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

    # 1. عنوان التطبيق
    self.title_label = Label(
        text="🤖 NIKLLIS-AI Assistant",
        font_size="24sp",
        bold=True,
        size_hint_y=None,
        height=50,
    )
    main_layout.add_widget(self.title_label)

    # 2. الروبوت المتحرك (Mascot)
    # هيفضل يتحرك فوق وتحت في وضع السكون (Idle Animation)
    self.robot_img = Image(
        source="robot_idle.gif", size_hint=(1, 0.4), allow_stretch=True
    )
    main_layout.add_widget(self.robot_img)
    self.animate_robot()

    # 3. حالة المساعد (Listening / Idle / Processing)
    self.status_label = Label(
        text="👋 أنا نكليس.. اضغط على المايك للتحدث",
        font_size="16sp",
        size_hint_y=None,
        height=40,
    )
    main_layout.add_widget(self.status_label)

    # 4. زر المايك الصوتي
    self.mic_btn = Button(
        text="🎙️ التحدث الآن",
        font_size="18sp",
        background_color=(0.2, 0.6, 1, 1),
        size_hint_y=None,
        height=60,
    )
    self.mic_btn.bind(on_press=self.on_mic_click)
    main_layout.add_widget(self.mic_btn)

    return main_layout

  def animate_robot(self):
    """عمل أنيميشن حركة الروبوت وقت السكون (Floating Effect)"""
    anim = Animation(y=10, duration=1.5) + Animation(y=-10, duration=1.5)
    anim.repeat = True
    anim.start(self.robot_img)

  def on_mic_click(self, instance):
    """عند الضغط على المايك"""
    self.status_label.text = "🎤 جاري الاستماع للأمر الصوتي..."
    # هنا بيتم استدعاء محرك الصوت من main.py
    Clock.schedule_once(self.reset_status, 4)

  def reset_status(self, dt):
    self.status_label.text = "✅ تم تنفيذ الأمر بنجاح!"


if __name__ == "__main__":
  NikllisApp().run()
