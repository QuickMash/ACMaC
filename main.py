import app.voice.tts as tts
import app.voice.input as voice_input
import app.assistant._ollama as _ollama

if __name__ == "__main__":
    while True:
        prompt = input("Enter your prompt: ")

        if prompt.strip().lower() == "/listen":
            captured = voice_input.listen_once()
            if not captured:
                continue
            print(f"You said: {captured}")
            prompt = captured

        response = _ollama.generate(prompt)
        print(response)
    #tts.generate(response)