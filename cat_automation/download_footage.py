"""
Module 3: download_footage.py
Downloads free cat stock videos from Pexels API.
Output: MP4 clips in output/footage/
"""

import requests
import os
import random
from config import PEXELS_API_KEY, PEXELS_QUERIES, OUTPUT_FOOTAGE


PEXELS_SEARCH_URL = "https://api.pexels.com/videos/search"


def search_cat_videos(query: str, per_page: int = 10) -> list[dict]:
    """Search Pexels for cat videos matching query."""
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": query,
        "per_page": per_page,
        "orientation": "portrait",   # Vertical for Shorts
        "size": "medium"
    }

    response = requests.get(PEXELS_SEARCH_URL, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Pexels error {response.status_code}: {response.text}")

    videos = response.json().get("videos", [])
    print(f"  🔍 Found {len(videos)} clips for: '{query}'")
    return videos


def get_best_video_file(video: dict) -> str | None:
    """Pick the best quality video file URL (HD preferred, not 4K)."""
    files = video.get("video_files", [])
    # Sort by resolution — prefer 1080x1920 or close
    portrait_files = [
        f for f in files
        if f.get("width", 0) <= 1080 and f.get("height", 0) >= 1080
    ]
    if not portrait_files:
        # Fallback: any file
        portrait_files = files

    if not portrait_files:
        return None

    # Pick highest quality under 1080p
    portrait_files.sort(key=lambda x: x.get("height", 0), reverse=True)
    return portrait_files[0]["link"]


def download_video(url: str, filepath: str) -> bool:
    """Download a video file to filepath. Returns True if successful."""
    if os.path.exists(filepath):
        print(f"  ⏭️  Skipping {os.path.basename(filepath)} (exists)")
        return True

    print(f"  ⬇️  Downloading {os.path.basename(filepath)}...")
    response = requests.get(url, stream=True, timeout=60)
    if response.status_code != 200:
        print(f"  ❌ Failed: {response.status_code}")
        return False

    with open(filepath, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    print(f"  ✅ Saved ({size_mb:.1f} MB)")
    return True


def download_footage_batch(num_clips: int = 30) -> list[str]:
    """
    Download `num_clips` cat video clips from Pexels.
    Rotates through all queries for variety.
    Returns list of local file paths.
    """
    os.makedirs(OUTPUT_FOOTAGE, exist_ok=True)
    downloaded = []
    clips_per_query = max(1, num_clips // len(PEXELS_QUERIES))

    print(f"\n📥 Downloading {num_clips} cat footage clips...")

    for query in PEXELS_QUERIES:
        videos = search_cat_videos(query, per_page=clips_per_query + 2)
        random.shuffle(videos)  # Avoid always getting same clips

        count = 0
        for video in videos:
            if count >= clips_per_query:
                break

            url = get_best_video_file(video)
            if not url:
                continue

            vid_id = video["id"]
            filepath = os.path.join(OUTPUT_FOOTAGE, f"cat_{vid_id}.mp4")

            if download_video(url, filepath):
                downloaded.append(filepath)
                count += 1

    print(f"\n✅ Total footage downloaded: {len(downloaded)} clips")
    return downloaded


def get_local_footage() -> list[str]:
    """Return all already-downloaded footage files."""
    if not os.path.exists(OUTPUT_FOOTAGE):
        return []
    return [
        os.path.join(OUTPUT_FOOTAGE, f)
        for f in os.listdir(OUTPUT_FOOTAGE)
        if f.endswith(".mp4")
    ]


if __name__ == "__main__":
    clips = download_footage_batch(num_clips=30)
    print(f"\n📁 Footage ready: {len(clips)} clips in {OUTPUT_FOOTAGE}")
