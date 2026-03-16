import speech_recognition as sr


def listen_once(timeout: int = 5, phrase_time_limit: int = 10) -> str | None:
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit,
            )
    except Exception as exc:
        print(f"Microphone error: {exc}")
        return None

    try:
        text = recognizer.recognize_google(audio)
        return text.strip()
    except sr.UnknownValueError:
        print("I couldn't understand that.")
        return None
    except sr.RequestError as exc:
        print(f"Speech service error: {exc}")
        return None