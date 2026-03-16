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
    
    elevenlabs.play(audio)
