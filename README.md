# 🐱 Cat YouTube Shorts Automation
### Fully Automated Cat Channel | From Script to Upload, All in One Click

---

## 📁 Project Structure
```
cat_automation/
├── main.py              ← Main entry point — runs the full pipeline
├── config.py            ← Fill in your API keys here
├── generate_scripts.py  ← Module 1: Generate scripts with Claude
├── generate_voice.py    ← Module 2: Voiceover with ElevenLabs
├── download_footage.py  ← Module 3: Download footage from Pexels
├── assemble_video.py    ← Module 4: Assemble videos with FFmpeg
├── upload_youtube.py    ← Module 5: Upload to YouTube
├── setup.bat            ← One-click installer for Windows
├── requirements.txt
└── output/
    ├── scripts/         ← Generated script JSON files
    ├── audio/           ← Voiceover MP3 files
    ├── footage/         ← Cat footage clips
    └── videos/          ← Final Shorts ready to upload
```
> **Recommended: log in via OpenClaw OAuth** — instead of pasting an API key, run:
> ```bash
> openclaw models auth login
---

## 🔑 Step 1: Get All API Keys

### 1. Pexels API Key (Free Stock Footage)
- Go to: https://www.pexels.com/api
- Sign up → Get Started → Request a free key
- Completely free, no usage limits
- Add to `config.py`: `PEXELS_API_KEY = "..."`

### 2. YouTube Data API (Video Uploads)
This step has a few more parts — follow along:

**Step A: Create a Google Cloud Project**
1. Go to https://console.cloud.google.com
2. Create a new project (any name works, e.g. "CatChannel")

**Step B: Enable the YouTube API**
1. Left menu → APIs & Services → Library
2. Search for "YouTube Data API v3" → Enable

**Step C: Create OAuth Credentials**
1. APIs & Services → Credentials
2. Create Credentials → OAuth client ID
3. Application type: **Web application**
4. Under **Authorized redirect URIs**, add the URL you'll redirect back to. **For Codespaces, see the section below first** — you'll need your codespace's forwarded URL here.
   - Local example: `http://localhost:8000/oauth2callback`
   - Codespaces example: `https://<your-codespace-name>-8000.app.github.dev/oauth2callback`
5. Click **Create**, then download the JSON file
6. Rename it to `client_secret.json` and place it in the project root directory
7. In `config.py`, set `YT_REDIRECT_URI` to the **same URL** you authorized above

> When you first run the upload step, the consent screen opens in your browser. After you click **Allow**, Google redirects back to your callback URL and the app saves the token locally.

---

## 💻 Running in GitHub Codespaces

This project is set up to run in **GitHub Codespaces** out of the box.

### Setup
```bash
# Inside the Codespace terminal:
pip install -r requirements.txt

# FFmpeg (Codespaces are Ubuntu-based)
sudo apt-get update && sudo apt-get install -y ffmpeg
```

### Important: forward port 8000 publicly
The OAuth callback needs Google's servers to reach your codespace, so port 8000 must be **public**:

1. Run any command that starts the callback server (or just `python main.py --skip-upload` once)
2. In VS Code's bottom panel, open the **Ports** tab
3. Find port `8000` → right-click → **Port Visibility → Public**
4. Copy the forwarded URL — it looks like `https://<codespace-name>-8000.app.github.dev`

### Configure the redirect URI
1. In Google Cloud Console → Credentials → your OAuth client → **Authorized redirect URIs**, add:
   `https://<your-codespace-name>-8000.app.github.dev/oauth2callback`
2. In `config.py`, set the same URL:
   ```python
   YT_REDIRECT_URI = "https://<your-codespace-name>-8000.app.github.dev/oauth2callback"
   ```

> ⚠️ Codespace URLs change if you delete and recreate the codespace. If that happens, update both Google Cloud Console **and** `config.py` with the new URL.

---

## 🚀 Step 2: Install and Run

### Codespaces Install (recommended for students)
```bash
pip install -r requirements.txt
sudo apt-get update && sudo apt-get install -y ffmpeg
```
Then follow the **Running in GitHub Codespaces** section above to forward port 8000 and set your redirect URI.

### Windows Install (local)
```bash
# 1. Double-click setup.bat
# Or from the command line:
pip install -r requirements.txt

# Install FFmpeg (pick one method)
winget install ffmpeg
# Or install manually from https://ffmpeg.org/download.html
```

### Run Order (test first — recommended)

```bash
# Step 1: Generate scripts only (free — test before spending money)
python main.py --scripts-only

# Step 2: Generate videos but don't upload (check quality)
python main.py --skip-upload --count 3

# Step 3: Full pipeline, 3 videos
python main.py --count 3

# Step 4: Real batch run, 10 videos
python main.py --count 10
```

---
