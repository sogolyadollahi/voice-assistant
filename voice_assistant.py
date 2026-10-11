
import pyttsx3
import speech_recognition as sr

from commands import (
    get_current_date,
    get_current_time,
    get_greeting,
    search_web,
)
from intent_parser import ParsedCommand, parse_intent


def listen_once() -> str:
    """Capture one utterance and convert it to text."""
    recognizer = sr.Recognizer()

    with sr.Microphone() as microphone:
        print("Listening... Speak now.")

        recognizer.adjust_for_ambient_noise(
            microphone,
            duration=0.5,
        )

        audio = recognizer.listen(
            microphone,
            timeout=5,
            phrase_time_limit=8,
        )

    return recognizer.recognize_google(
        audio,
        language="en-US",
    )


def speak(text: str, engine) -> None:
    """Speak a response using the local speech engine."""
    engine.say(text)
    engine.runAndWait()


def execute_command(command: ParsedCommand) -> str:
    """Dispatch a parsed command to its handler."""
    if command.intent == "greeting":
        return get_greeting()

    if command.intent == "time":
        return get_current_time()

    if command.intent == "date":
        return get_current_date()

    if command.intent == "search":
        query = command.entities.get("query", "")
        return search_web(query)

    if command.intent == "exit":
        return "Goodbye!"

    return "I didn't understand that command. Please try again."


def main() -> None:
    """Run the continuous voice assistant loop."""
    engine = pyttsx3.init()

    try:
        speak("Voice assistant is ready.", engine)

        while True:
            try:
                text = listen_once()
                print(f"Recognized: {text}")

                command = parse_intent(text)
                response = execute_command(command)

                print(f"Assistant: {response}")
                speak(response, engine)

                if command.intent == "exit":
                    break

            except sr.WaitTimeoutError:
                print("No speech detected. Listening again.")

            except sr.UnknownValueError:
                speak(
                    "I couldn't understand that. Please repeat.",
                    engine,
                )

            except sr.RequestError as error:
                print(f"Speech recognition error: {error}")
                speak(
                    "Speech recognition is unavailable. Check your connection.",
                    engine,
                )

            except OSError as error:
                print(f"Audio or operating system error: {error}")
                speak(
                    "There was an audio error. Please check your microphone.",
                    engine,
                )
                break

    except KeyboardInterrupt:
        print("\nStopping assistant.")

    finally:
        engine.stop()


if __name__ == "__main__":
    main()
