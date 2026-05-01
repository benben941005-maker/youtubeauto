"""
Module 4: assemble_video.py
Uses FFmpeg to assemble:
  - Cat footage clips (looped/trimmed to match audio)
  - ElevenLabs voiceover
  - Bilingual subtitles (EN top + ZH bottom)
Output: Final MP4 Shorts in output/videos/
"""

import subprocess
import os
import json
import random
import tempfile
from pathlib import Path
from config import (
    VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS, OUTPUT_VIDEOS,
    FFMPEG_BIN, FFPROBE_BIN
)


def generate_srt(subtitle_lines: list[dict], audio_duration: float) -> str:
    """
    Generate SRT subtitle content from script subtitle_lines.
    Evenly distributes lines across the audio duration.
    Each entry has both EN and ZH lines.
    """
    srt = ""
    n = len(subtitle_lines)
    interval = audio_duration / n

    for i, line in enumerate(subtitle_lines):
        start = i * interval
        end = min((i + 1) * interval, audio_duration)

        def fmt_time(secs):
            h = int(secs // 3600)
            m = int((secs % 3600) // 60)
            s = int(secs % 60)
            ms = int((secs - int(secs)) * 1000)
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

        en = line.get("en", "")
        zh = line.get("zh", "")
        srt += f"{i+1}\n{fmt_time(start)} --> {fmt_time(end)}\n{en}\n{zh}\n\n"

    return srt


def get_audio_duration(audio_path: str) -> float:
    """Get duration of audio file in seconds."""
    result = subprocess.run([
        FFPROBE_BIN, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ], capture_output=True, text=True)
    return float(result.stdout.strip())


def build_video_concat_list(footage_files: list[str], target_duration: float, tmpdir: str) -> str:
    """
    Build an FFmpeg concat file that loops footage clips
    until total duration >= target_duration.
    """
    concat_path = os.path.join(tmpdir, "concat.txt")
    total = 0.0
    entries = []

    random_clips = footage_files.copy()
    random.shuffle(random_clips)

    # Repeat clips if needed
    while total < target_duration:
        for clip in random_clips:
            # Get clip duration
            result = subprocess.run([
                FFPROBE_BIN, "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                clip
            ], capture_output=True, text=True)
            try:
                dur = float(result.stdout.strip())
            except ValueError:
                continue

            entries.append(clip)
            total += dur
            if total >= target_duration:
                break

    with open(concat_path, "w", encoding="utf-8") as f:
        for clip in entries:
            # Use absolute paths so FFmpeg concat works from temp dirs
            safe_path = os.path.abspath(clip).replace("\\", "/")
            f.write(f"file '{safe_path}'\n")

    return concat_path


def assemble_short(script: dict, footage_files: list[str], output_path: str) -> str:
    """
    Build a single YouTube Short from script + footage + voice.
    Returns path to final MP4.
    """
    if os.path.exists(output_path):
        print(f"  ⏭️  Skipping (exists): {os.path.basename(output_path)}")
        return output_path

    audio_path = script.get("audio_path")
    if not audio_path or not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio not found for script {script['id']}")

    subtitle_lines = script.get("subtitle_lines", [])
    audio_duration = get_audio_duration(audio_path)

    print(f"  🎬 Assembling video {script['id']}: {audio_duration:.1f}s")

    with tempfile.TemporaryDirectory() as tmpdir:

        # --- Step 1: Concat footage to match audio duration ---
        concat_file = build_video_concat_list(footage_files, audio_duration + 1, tmpdir)
        raw_video = os.path.join(tmpdir, "raw_video.mp4")

        subprocess.run([
            FFMPEG_BIN, "-y",
            "-f", "concat", "-safe", "0",
            "-i", concat_file,
            "-t", str(audio_duration),
            "-vf", f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=increase,"
                   f"crop={VIDEO_WIDTH}:{VIDEO_HEIGHT},"
                   f"fps={VIDEO_FPS}",
            "-an",  # No audio from footage
            "-c:v", "libx264", "-preset", "ultrafast",
            raw_video
        ], check=True, capture_output=True)

        # --- Step 2: Write SRT subtitle file ---
        srt_content = generate_srt(subtitle_lines, audio_duration)
        srt_path = os.path.join(tmpdir, "subs.srt")
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(srt_content)

        # --- Step 3: Burn subtitles + add voiceover ---
        safe_srt = srt_path.replace("\\", "/").replace(":", "\\:")

        # Subtitle style: EN white top, ZH yellow bottom
        subtitle_filter = (
            f"subtitles='{safe_srt}':force_style='"
            f"FontName=Arial,FontSize=18,PrimaryColour=&HFFFFFF,"
            f"OutlineColour=&H000000,Outline=2,Alignment=2,"
            f"MarginV=80'"
        )

        subprocess.run([
            FFMPEG_BIN, "-y",
            "-i", raw_video,
            "-i", audio_path,
            "-vf", subtitle_filter,
            "-c:v", "libx264", "-preset", "ultrafast",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            output_path
        ], check=True, capture_output=True)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"  ✅ Video done: {os.path.basename(output_path)} ({size_mb:.1f} MB)")
    return output_path


def assemble_all_videos(scripts: list[dict], footage_files: list[str]) -> list[dict]:
    """Assemble a Short for every script. Adds 'video_path' to each script."""
    os.makedirs(OUTPUT_VIDEOS, exist_ok=True)

    if not footage_files:
        raise ValueError("No footage files found. Run download_footage.py first.")

    print(f"\n🎬 Assembling {len(scripts)} videos...")

    for script in scripts:
        sid = script["id"]
        out_path = os.path.join(OUTPUT_VIDEOS, f"short_{sid:03d}.mp4")
        try:
            script["video_path"] = assemble_short(script, footage_files, out_path)
        except Exception as e:
            print(f"  ❌ Error on script {sid}: {e}")
            script["video_path"] = None

    done = [s for s in scripts if s.get("video_path")]
    print(f"\n✅ {len(done)}/{len(scripts)} videos assembled!")
    return scripts


if __name__ == "__main__":
    from generate_scripts import load_latest_scripts
    from download_footage import get_local_footage

    scripts = load_latest_scripts()
    footage = get_local_footage()
    scripts = assemble_all_videos(scripts, footage)
