import time
import speech_recognition as sr

def listen_command():
    """الاستماع للصوت وتحويله إلى نص عالي الدقة"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 جاري الاستماع للأمر...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        # التعرف على الكلام باللغة العربية
        command = recognizer.recognize_google(audio, language="ar-EG")
        print(f"🗣️ تم التعرف على النص: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("⚠️ لم أتمكن من فهم الصوت، حاول مرة أخرى.")
        return ""
    except sr.RequestError:
        print("❌ خطأ في الاتصال بخدمة التعرف على الصوت.")
        return ""

def process_command(command):
    """تحليل الأمر وإرساله للوظيفة المناسبة"""
    if "رن على" in command or "اتصل ب" in command:
        target = command.replace("رن على", "").replace("اتصل ب", "").strip()
        print(f"📞 جارٍ تنفيذ الاتصال بـ: {target}")
        # TODO: ربط كود الاتصال

    elif "نزل" in command or "بوست" in command:
        print("📅 جارٍ معالجة جدولة المنشور على فيسبوك...")
        # TODO: ربط كود Facebook Graph API

    else:
        print("🤖 لم يتم التكليف بأمر خاص، الروبوت في وضع السكون/اللعب (Idle Mode)")

if __name__ == "__main__":
    print("🚀 بدء تشغيل المساعد الذكي NIKLLIS-AI...")
    while True:
        user_cmd = listen_command()
        if user_cmd:
            process_command(user_cmd)
        time.sleep(1)
