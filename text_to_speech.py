# text_to_speech.py
# Converts text into speech using ElevenLabs API and saves as audio.mp3

import os
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from config import ELEVENLABS_API_KEY

# Initialize ElevenLabs client with your API key
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def text_to_speech_file(text: str, folder: str) -> str:
    """
    Converts the given text to speech and saves it as audio.mp3 in user_uploads/<folder>
    Returns the path of the saved audio file.
    """

    # Ensure folder exists
    os.makedirs(f"user_uploads/{folder}", exist_ok=True)

    # Call ElevenLabs text-to-speech API
    response = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB",  # Adam voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
            speed=1.0,
        ),
    )

    # Save audio to file
    save_file_path = os.path.join(f"user_uploads/{folder}", "audio.mp3")
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")
    return save_file_path
