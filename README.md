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

---

## 🔑 Step 1: Get All API Keys

### 1. Claude API Key (Anthropic)
- Go to: https://console.anthropic.com
- Sign up → API Keys → Create Key
- Free tier: $5 in trial credit
- Add to `config.py`: `CLAUDE_API_KEY = "sk-ant-..."`

### 2. ElevenLabs API Key (AI Voiceover)
- Go to: https://elevenlabs.io
- Sign up for a free account → Profile → API Key
- Free tier: 10,000 characters per month (about 10 videos)
- Add to `config.py`: `ELEVENLABS_API_KEY = "..."`

### 3. Pexels API Key (Free Stock Footage)
- Go to: https://www.pexels.com/api
- Sign up → Get Started → Request a free key
- Completely free, no usage limits
- Add to `config.py`: `PEXELS_API_KEY = "..."`

### 4. YouTube Data API (Video Uploads)
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
3. Application type: **Desktop app**
4. Download the JSON file
5. Rename it to `client_secret.json`
6. Place it in the project root directory

---

## 🚀 Step 2: Install and Run

### Windows Install
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

## 💰 Affiliate Setup

Add your affiliate link to `config.py`:
```python
AFFILIATE_LINK = "https://shopee.sg/your-affiliate-link"
```

**How to sign up for Shopee/Lazada Affiliate programs:**
- Shopee: https://affiliate.shopee.sg → Sign up → Get your tracking link
- Lazada: https://affiliate.lazada.com.sg → Same process
- Recommended products: cat litter, cat toys, cat food, cat trees

---

## ⏰ Run Daily Automatically (Windows Task Scheduler)

```bash
# In Windows Task Scheduler, set up a daily run:
# Action → Program: python
# Arguments: C:\path\to\cat_automation\main.py --count 2
# Trigger: Daily at 09:00
```

---

## 📊 Expected Revenue Timeline

| Month | Videos | Expected Subs | Income Source |
|-------|--------|---------------|---------------|
| Month 1 | 60 | 100–300 | Affiliate kicks in |
| Month 2 | 120 | 300–800 | Affiliate $50–200 |
| Month 3 | 180 | 800–2,000 | Apply for YPP |
| Month 4+ | 240+ | 1,000+ | AdSense + Affiliate |

---

## ❓ FAQ

**Q: FFmpeg not found?**
A: Run `winget install ffmpeg`, then restart your terminal.

**Q: ElevenLabs free tier used up?**
A: Upgrade to the $5/month Starter plan (110,000 characters).

**Q: YouTube upload failing?**
A: Delete `youtube_token.pickle` and re-authorize.

**Q: Can the stock footage be used commercially?**
A: Yes — Pexels videos are free for commercial use, no attribution required.

---

*Built with Claude + ElevenLabs + Pexels + FFmpeg + YouTube API*
