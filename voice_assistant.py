VOICE_SUPPORTED = [
    "English",
    "Kannada",
    "Hindi",
    "Tamil",
    "Telugu"
]


def voice_instructions():

    return """
Voice Assistant:

1. Use the microphone input available in the browser.
2. Convert speech to text using the browser speech-recognition
   capability where supported.
3. Send only the resulting text to GovAssist AI.
4. Never transmit passwords, OTPs or PINs.
5. Display the recognized text before processing.
"""


def browser_voice_html():

    return """
<script>

const recognitionSupported =
    'webkitSpeechRecognition' in window ||
    'SpeechRecognition' in window;

function startGovAssistVoice() {

    if (!recognitionSupported) {

        alert(
            "Speech recognition is not supported "
            + "by this browser."
        );

        return;
    }

    const Recognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    const recognition =
        new Recognition();

    recognition.lang = "en-IN";

    recognition.interimResults = false;

    recognition.continuous = false;

    recognition.onresult = function(event) {

        const text =
            event.results[0][0].transcript;

        navigator.clipboard.writeText(text);

        alert(
            "Recognized speech copied. "
            + "Paste it into the GovAssist AI input."
        );
    };

    recognition.onerror = function() {

        alert(
            "Voice recognition failed. "
            + "Please try again."
        );
    };

    recognition.start();
}

</script>

<button
    onclick="startGovAssistVoice()"
    style="
        padding:12px 18px;
        border-radius:10px;
        border:none;
        cursor:pointer;
        font-weight:600;
    "
>
🎤 Speak to GovAssist
</button>
"""
