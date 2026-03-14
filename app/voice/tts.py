from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import os

load_dotenv()

elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

def generate(text: str, voice_id: str = "JBFqnCBsd6RMkjVDRZzb", model_id: str = "eleven_multilingual_v2"):
    audio = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
        output_format="mp3_44100_128",
    )

    output_path = os.path.join(os.path.dirname(__file__), "output.mp3")

    with open(output_path, "wb") as audio_file:
      for chunk in audio:
        audio_file.write(chunk)

    print(f"Saved audio to {output_path}")
