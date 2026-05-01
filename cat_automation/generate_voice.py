"""
Module 2: generate_voice.py
Generates English MP3 voiceovers.
Default provider: Edge TTS (free)
Optional provider: ElevenLabs
Output: MP3 files in output/audio/
"""

import asyncio
import os
import requests
from config import (
    TTS_PROVIDER, EDGE_TTS_VOICE,
    ELEVENLABS_API_KEY, VOICE_ID, ELEVENLABS_MODEL_ID,
    VOICE_STABILITY, VOICE_SIMILARITY, OUTPUT_AUDIO,
    FFPROBE_BIN
)


async def _edge_tts_save(text: str, filepath: str) -> None:
    import edge_tts
    communicate = edge_tts.Communicate(text=text, voice=EDGE_TTS_VOICE)
    await communicate.save(filepath)


def text_to_speech_edge(text: str, filename: str) -> str:
    os.makedirs(OUTPUT_AUDIO, exist_ok=True)
    filepath = os.path.join(OUTPUT_AUDIO, filename)
    print(f"  🎙️  Generating voice with Edge TTS: {filename}...")
    asyncio.run(_edge_tts_save(text, filepath))
    print(f"  ✅ Audio saved: {filepath}")
    return filepath


def text_to_speech_elevenlabs(text: str, filename: str) -> str:
    os.makedirs(OUTPUT_AUDIO, exist_ok=True)
    filepath = os.path.join(OUTPUT_AUDIO, filename)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": ELEVENLABS_MODEL_ID,
        "voice_settings": {
            "stability": VOICE_STABILITY,
            "similarity_boost": VOICE_SIMILARITY
        }
    }

    print(f"  🎙️  Generating voice with ElevenLabs: {filename}...")
    response = requests.post(url, headers=headers, json=payload, timeout=120)

    if response.status_code != 200:
        raise Exception(f"ElevenLabs error {response.status_code}: {response.text}")

    with open(filepath, "wb") as f:
        f.write(response.content)

    print(f"  ✅ Audio saved: {filepath}")
    return filepath


def text_to_speech(text: str, filename: str) -> str:
    provider = (TTS_PROVIDER or "edge").lower()
    if provider == "elevenlabs":
        return text_to_speech_elevenlabs(text, filename)
    return text_to_speech_edge(text, filename)


def generate_all_voices(scripts: list[dict]) -> list[dict]:
    """
    Generate MP3 for each script.
    Adds 'audio_path' key to each script dict.
    """
    print(f"\n🎙️  Generating {len(scripts)} voiceovers...")

    for script in scripts:
        sid = script["id"]
        filename = f"voice_{sid:03d}.mp3"
        audio_path = os.path.join(OUTPUT_AUDIO, filename)

        if os.path.exists(audio_path):
            print(f"  ⏭️  Skipping {filename} (already exists)")
            script["audio_path"] = audio_path
            continue

        script["audio_path"] = text_to_speech(
            text=script["script_en"],
            filename=filename
        )

    print("✅ All voiceovers done!")
    return scripts


def get_audio_duration(filepath: str) -> float:
    """Get MP3 duration in seconds using ffprobe."""
    import subprocess
    result = subprocess.run([
        FFPROBE_BIN, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        filepath
    ], capture_output=True, text=True)
    return float(result.stdout.strip())


if __name__ == "__main__":
    import os
    from generate_scripts import load_latest_scripts

    scripts = load_latest_scripts()
    scripts = generate_all_voices(scripts)

    for s in scripts[:3]:
        if "audio_path" in s and os.path.exists(s["audio_path"]):
            print(f"  Script {s['id']}: {s['title_en']}")
