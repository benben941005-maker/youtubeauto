"""
🐱 Cat YouTube Automation - Main Pipeline
==========================================
Run this file to execute the full automation:
  1. Generate scripts (Claude API)
  2. Generate voiceover (ElevenLabs)
  3. Download cat footage (Pexels)
  4. Assemble videos (FFmpeg)
  5. Upload to YouTube (YouTube API)

Usage:
  python main.py                    # Full run (10 videos)
  python main.py --count 5          # Generate 5 videos
  python main.py --skip-upload      # Stop before YouTube upload
  python main.py --scripts-only     # Only generate scripts
"""

import argparse
import json
import os
import sys
from datetime import datetime


def log(msg: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}")


def save_session(scripts: list[dict], session_file: str = "session.json"):
    """Save current pipeline state to resume if something fails."""
    with open(session_file, "w", encoding="utf-8") as f:
        json.dump(scripts, f, ensure_ascii=False, indent=2)


def load_session(session_file: str = "session.json") -> list[dict] | None:
    """Load a previous session to resume from where we left off."""
    if os.path.exists(session_file):
        with open(session_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def run_pipeline(count: int = 10, skip_upload: bool = False, scripts_only: bool = False):
    print("\n" + "="*50)
    print("🐱 CAT YOUTUBE AUTOMATION PIPELINE")
    print("="*50 + "\n")

    # ── STEP 1: Generate Scripts ──────────────────────
    log("📝 STEP 1/5 — Generating scripts with Claude...")
    from generate_scripts import generate_scripts, save_scripts
    scripts = generate_scripts(count=count)
    save_scripts(scripts)
    save_session(scripts)
    log(f"✅ {len(scripts)} scripts generated\n")

    if scripts_only:
        log("--scripts-only flag set. Stopping here.")
        return

    # ── STEP 2: Generate Voiceovers ───────────────────
    log("🎙️  STEP 2/5 — Generating voiceovers with ElevenLabs...")
    from generate_voice import generate_all_voices
    scripts = generate_all_voices(scripts)
    save_session(scripts)
    log("✅ Voiceovers done\n")

    # ── STEP 3: Download Footage ──────────────────────
    log("📥 STEP 3/5 — Downloading cat footage from Pexels...")
    from download_footage import download_footage_batch, get_local_footage
    existing = get_local_footage()
    if len(existing) < count * 3:
        download_footage_batch(num_clips=count * 4)
    footage_files = get_local_footage()
    log(f"✅ {len(footage_files)} footage clips ready\n")

    # ── STEP 4: Assemble Videos ───────────────────────
    log("🎬 STEP 4/5 — Assembling final videos with FFmpeg...")
    from assemble_video import assemble_all_videos
    scripts = assemble_all_videos(scripts, footage_files)
    save_session(scripts)
    done = [s for s in scripts if s.get("video_path")]
    log(f"✅ {len(done)} videos assembled\n")

    if skip_upload:
        log("--skip-upload flag set. Videos saved locally.")
        log(f"📁 Check: output/videos/")
        return

    # ── STEP 5: Upload to YouTube ─────────────────────
    log("📤 STEP 5/5 — Uploading to YouTube...")
    from upload_youtube import upload_all_videos
    scripts = upload_all_videos(scripts)
    save_session(scripts)

    # ── SUMMARY ───────────────────────────────────────
    uploaded = [s for s in scripts if s.get("youtube_id")]
    print("\n" + "="*50)
    print(f"🎉 PIPELINE COMPLETE!")
    print(f"   Videos generated : {len(done)}")
    print(f"   Videos uploaded  : {len(uploaded)}")
    print("="*50)
    print("\n🔗 Your new Shorts:")
    for s in uploaded:
        print(f"   [{s['id']}] {s['youtube_url']}")
        print(f"        {s['title_en']}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cat YouTube Automation Pipeline")
    parser.add_argument("--count", type=int, default=10, help="Number of videos to generate")
    parser.add_argument("--skip-upload", action="store_true", help="Don't upload to YouTube")
    parser.add_argument("--scripts-only", action="store_true", help="Only generate scripts")
    args = parser.parse_args()

    run_pipeline(
        count=args.count,
        skip_upload=args.skip_upload,
        scripts_only=args.scripts_only
    )
