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

## 💬 Run It from Telegram (fully chat-driven workflow)

Once your OpenClaw + Telegram bot is paired, the entire workflow happens in chat. You paste a GitHub link, the bot patches it for Codespaces, and from then on you just say **"make 1 short"** and approve a title + script — the bot handles voice, footage, video assembly, and YouTube upload.

### Step 1 — First-contact prompt (persona setup)
The very first time you message a fresh OpenClaw agent, it will ask for **its name, creature, vibe, and emoji** before doing anything else. Paste this as your first message to skip the back-and-forth:

> **Hi! Quick setup so we can skip the questions:**
>
> - Call me **`<your name>`** (e.g. Pinky)
> - You are **`Little Cat`**, a calm and observant assistant
> - Vibe: calm, blunt, helpful — short replies, no fluff
> - Signature emoji: 🐱
>
> Confirm with one short message and we're done with intros.

### Step 2 — Bootstrap prompt (paste the GitHub link, bot patches everything)
This is the prompt that sets up the whole project automatically. Just swap in your repo URL:

> **Here's the project: `https://github.com/<your-username>/youtubeauto`**
>
> Please do the following automatically and tell me when each step is done:
>
> 1. **Clone it** into `/home/codespace/.openclaw/workspace/youtubeauto`.
> 2. **Patch it for Codespaces:**
>    - Replace `tools/ffmpeg/ffmpeg` and `tools/ffmpeg/ffprobe` with system binaries (`ffmpeg`, `ffprobe`).
>    - Make `YT_REDIRECT_URI` use my Codespaces forwarded URL on port 8000.
>    - Add env var fallbacks for `ANTHROPIC_API_KEY`, `PEXELS_API_KEY`, `ELEVENLABS_API_KEY`.
>    - `pip install -r requirements.txt` and `sudo apt-get install -y ffmpeg`.
> 3. **Patch script generation to use OpenClaw model auth** — remove the hard dependency on the Anthropic SDK and route script generation through `openclaw infer model run --gateway --json`. Add `SCRIPT_MODEL` in `config.py` for an explicit override.
> 4. **Verify** by running:
>    ```
>    openclaw infer model run --gateway --prompt "Reply with exactly: pong" --json
>    ```
>    Tell me if it returns `pong`.
> 5. Confirm port 8000 is **Public** in the Ports tab.
> 6. Wait for me to upload my Google `client_secret.json` and tell you my Pexels key — then we're ready.

### Step 3 — Operating prompt (the actual day-to-day rules)
After bootstrap is done, paste this so the bot knows how to behave on every short:

> **From now on, you run my YouTube cat-shorts pipeline for me.**
> Project folder: `/home/codespace/.openclaw/workspace/youtubeauto/cat_automation`
>
> When I say **"make N short(s)"**, do this in order — pause for my approval each time:
>
> 1. **Suggest 3 title options** (English + Chinese), based on the channel niche. Wait for me to reply with `title 1` / `title 2` / `title 3` — or `more titles` to regenerate.
> 2. Once a title is approved, **generate the full script** (hook + 3 facts + CTA, ~40–45 seconds, bilingual) using OpenClaw model auth. Send me the script. Wait for `approve` / `tweak <feedback>` / `regenerate`.
> 3. Once the script is approved, **run the rest of the pipeline silently**: voice → footage → assemble → upload to YouTube.
> 4. Reply with the final **YouTube Shorts URL** when done.
> 5. If anything fails, summarize the error in plain English and propose a fix.
> 6. Never paste real API keys or `client_secret.json` contents back to me — treat them as private.
> 7. If Google OAuth needs consent, send me the auth URL and pause until I click Allow.

> 💡 **Combine all 3 prompts into one message** to skip the back-and-forth entirely. The bot will work through them in order.

### What a session actually looks like

```
You:   make 1 short
Bot:   Here are 3 title options:
       1. 3 Cat Litter Mistakes You're Making 😱  
       2. Why Your Cat Ignores That Expensive Toy 
       3. The Truth About Cat Grooming 
You:   title 2
Bot:   Script for title 2:
       Hook: Did you know most cat owners waste money on toys cats hate?
       ... (full bilingual script)
       Approve / tweak / regenerate?
You:   approve
Bot:   ✅ voice generated
       ✅ footage downloaded
       ✅ video assembled
       ✅ uploaded
       https://youtube.com/shorts/abc123
```

### Day-to-day commands

| You say | Bot does |
|---|---|
| `make 1 short` | Suggests 3 titles → script approval → uploads |
| `make 3 shorts` | Repeats the title→script→upload cycle 3 times |
| `more titles` | Regenerates 3 new title options |
| `tweak: make hook funnier` | Regenerates the script with your feedback |
| `regenerate` | Tries the current step again from scratch |
| `draft only` | Stops after script approval, doesn't upload |
| `upload latest` | Uploads the most recently approved draft |
| `show status` | Lists the latest scripts/videos and their stage |
| `show latest video` | Sends the most recent assembled `.mp4` |
| `clean up` | Deletes old footage/audio/scripts to free space |
| `what failed?` | Explains the last error in plain language |

### Tips
- **First upload only** triggers a Google OAuth consent screen — the bot pastes the auth URL, you click Allow once, and the token is reused after that until it expires.
- The bot runs inside your Codespace, so the codespace must be **running** when you message it. (Codespaces sleep after inactivity — just open the tab to wake it.)
- If your Codespace URL changes, tell the bot: **"my codespace URL is now https://...-8000.app.github.dev — update YT_REDIRECT_URI"** and it will patch `config.py` for you.
- Treat any client secret or API key that passed through chat as **exposed** — rotate it in Google Cloud / your provider after setup.

---
## ❓ FAQ


**Q: Telegram pairing fails with `Cannot find module 'grammy'`?**
A: OpenClaw's bundled Telegram channel needs the `grammy` Node.js library. Install it globally:
```bash
sudo npm install -g grammy
