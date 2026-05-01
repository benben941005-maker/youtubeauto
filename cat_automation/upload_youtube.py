"""
Module 5: upload_youtube.py
Authenticates with YouTube Data API and uploads finished Shorts.
Requires: client_secret.json from Google Cloud Console
"""

import os
import json
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from config import YOUTUBE_SECRET_FILE, YT_CATEGORY_ID, YT_PRIVACY, YT_TAGS

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE = "youtube_token.pickle"


def get_youtube_client():
    """Authenticate and return YouTube API client. Opens browser on first run."""
    creds = None

    # Reuse saved token if available
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                YOUTUBE_SECRET_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)

    return build("youtube", "v3", credentials=creds)


def upload_short(youtube, script: dict) -> str | None:
    """
    Upload a single Short to YouTube.
    Returns the YouTube video ID if successful.
    """
    video_path = script.get("video_path")
    if not video_path or not os.path.exists(video_path):
        print(f"  ❌ Video file not found for script {script['id']}")
        return None

    # Use bilingual title: English first, Chinese in brackets
    title = f"{script['title_en']} | {script['title_zh']}"[:100]

    # Bilingual description with affiliate link
    description = (
        f"{script['description_en']}\n\n"
        f"{'='*30}\n\n"
        f"{script['description_zh']}\n\n"
        f"#cats #猫咪 #shorts #catshorts #可爱猫咪 #cattips"
    )

    tags = list(set(YT_TAGS + script.get("tags", [])))

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": YT_CATEGORY_ID,
            "defaultLanguage": "en",
        },
        "status": {
            "privacyStatus": YT_PRIVACY,
            "selfDeclaredMadeForKids": False,
        }
    }

    print(f"  📤 Uploading: {title[:60]}...")

    media = MediaFileUpload(
        video_path,
        mimetype="video/mp4",
        resumable=True,
        chunksize=1024 * 1024  # 1MB chunks
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            print(f"    Upload progress: {pct}%", end="\r")

    video_id = response["id"]
    url = f"https://youtube.com/shorts/{video_id}"
    print(f"\n  ✅ Uploaded! {url}")
    return video_id


def upload_all_videos(scripts: list[dict]) -> list[dict]:
    """Upload all assembled videos to YouTube."""
    to_upload = [s for s in scripts if s.get("video_path") and not s.get("youtube_id")]

    if not to_upload:
        print("No new videos to upload.")
        return scripts

    print(f"\n📤 Uploading {len(to_upload)} videos to YouTube...")
    youtube = get_youtube_client()

    for script in to_upload:
        youtube_id = upload_short(youtube, script)
        script["youtube_id"] = youtube_id
        script["youtube_url"] = f"https://youtube.com/shorts/{youtube_id}" if youtube_id else None

    done = [s for s in scripts if s.get("youtube_id")]
    print(f"\n✅ Uploaded {len(done)} videos!")
    return scripts


if __name__ == "__main__":
    from generate_scripts import load_latest_scripts
    scripts = load_latest_scripts()
    scripts = upload_all_videos(scripts)
