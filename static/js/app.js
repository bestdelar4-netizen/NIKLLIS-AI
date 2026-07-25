let recognition;
let listening = false;

const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
    recognition = new SpeechRecognition();

    recognition.lang = "ar-EG";
    recognition.continuous = true;
    recognition.interimResults = false;

    recognition.onstart = () => {
        listening = true;
        document.getElementById("status").innerText = "🎤 أستمع إليك...";
    };

    recognition.onresult = async (event) => {

        let text = event.results[event.results.length - 1][0].transcript;

        document.getElementById("user").innerText = "أنت: " + text;

        let res = await fetch("/process?cmd=" + encodeURIComponent(text));
        let data = await res.json();

        document.getElementById("reply").innerText =
            "NIKLLIS: " + data.reply;

        let voice = new SpeechSynthesisUtterance(data.reply);
        voice.lang = "ar-EG";
        speechSynthesis.speak(voice);
    };

    recognition.onerror = () => {};

    recognition.onend = () => {
        if (listening) {
            recognition.start();
        }
    };
}

function startListening() {
    if (!listening) {
        recognition.start();
    }
}

function stopListening() {
    listening = false;
    recognition.stop();
}