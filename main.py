import speech_recognition as sr
import asyncio
import pyttsx3
from googletrans import Translator

# Initilize text to speach enginesync
def speak(text, language='en'):
    engine = None
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        voices = engine.getProperty("voices")
        # try to find a voice matching requested language
        language = language.lower()
        for voice in voices:
            voice_info = (
                str(voice.id) + " " + str(voice.name) + " " + str(voice.languages)
            ).lower()
            if language in voice_info:
                engine.setProperty("voice", voice.id)
                break
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Text-To-Speech Error: {e}")

    finally:
        if engine:
            engine.stop()

def speech_to_text():
    recognizer = sr.Recognizer()

    recognizer.pause_threshold = 2.5
    recognizer.dynamic_energy_threshold = True
    recognizer.non_speaking_duration = 0.5

    try:
        with sr.Microphone() as source:
            print("\nCalibrating microphone... Please wait")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            print("\nMicrophone ready!")
            print("Start speaking inEnglish...")
            print("You have up to 30 seconds.")

            audio = recognizer.listen(
                source,
                timeout=None,
                phrase_time_limit=30
            )

        print("\nRecognizing speech....")

        text = recognizer.recognize_google(
            audio,
            language="en-US"
        )

        print(f"\nYou said: {text}")
        return text

    except sr.UnknownValueError:
        print("Could not understand the audio.")

    except sr.RequestError as e:
        print(f"Speech recognition API error: {e}")

    except OSError as e:
        print(f"Microphone error: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")


    return ""

# transleate text using google translate api
async def async_translate_text(text, target_language):
    async with Translator() as translator:
        translation = await translator.translate(
            text,
            dest=target_language
        )
        return translation.text

def translate_text(text, target_language="es"):
    try:
        translated_text = asyncio.run(
            async_translate_text(text, target_language)
        )
        print(f"Translated text: {translated_text}")
        return translated_text

    except Exception as e:
        print(f"Translation error: {e}")
        return ""

# display language options to the user
def display_language_options():
    print("\nAvailable translation languages:")
    print("1. Hindi (hi)")
    print("2. Tamil (ta)")
    print("3. Telugu (te)")
    print("4. Bengali (bn)")
    print("5. Marathi (mr)")
    print("5. Gujarati (gu)")
    print("6. Malayalam (mi)")
    print("7. Punjabi (pa)")
    print("8. Japanese (ja)")
    print("9. French (fr)")
    print("10. Spanish (es)")
    print("11. German (de)")
    print("13. Chinese (zh-cn)")
    print("14. Korean (ko)")
    print("15. Italian (it)")
    print("16. Portuguese (pt)")

    language_dict = {
        "1": "hi",
        "2": "ta",
        "3": "te",
        "4": "bn",
        "5": "mr",
        "6": "gu",
        "7": "mi",
        "8": "pa",
        "9": "ja",
        "10": "fr",
        "11": "es",
        "12": "de",
        "13": "zh-cn",
        "14": "ko",
        "15": "it",
        "16": "pt",
    }

    choice = input("\nSelect a target language (1-16): ").strip()
    if choice not in language_dict:
        print("Invalid selection. Defaulting to Spanish.")
    return language_dict.get(choice, "es")

# main function to combine all of the steps

def main():
    target_language = display_language_options()
    original_text = speech_to_text()

    if not original_text:
        print("\nNo speech was recognized. Please try again.")
        return

    # speak the original English words
    print("\nSpeaking your original words...")
    speak(original_text, language="en")


    # translate the original words
    translated_text = translate_text(
        original_text,
        target_language=target_language
    )

    if not translated_text:
        print("\nTranslation failed. Please try agian.")
        return
    # speak the translated text
    print("\nSpeaking the translated text...")
    speak(translated_text, language=target_language)

    print("\nTranslation spoken out!")


if __name__ == "__main__":
    main()
