# ============================================================
# 🐱 Cat YouTube Automation - Config
# Fill in your API keys below before running!
# ============================================================

# --- API KEYS (see README.md on how to get each one) ---
CLAUDE_API_KEY      = ""          # not used for the manual approval flow
ELEVENLABS_API_KEY  = "xxxx"                  # elevenlabs.io
PEXELS_API_KEY      = "xxxx"                  # pexels.com/api
YOUTUBE_SECRET_FILE = "client_secret.json"    # Google Cloud Console
YT_REDIRECT_URI    = "xxxx"   # e.g. http://localhost:8000/oauth2callback
YT_CALLBACK_HOST   = "0.0.0.0"
YT_CALLBACK_PORT   = 8000

# --- Voice Settings ---
# Free default voice path: Microsoft Edge TTS
TTS_PROVIDER = "edge"
EDGE_TTS_VOICE = "en-US-AvaMultilingualNeural"

# Optional ElevenLabs settings if you switch back later
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
ELEVENLABS_MODEL_ID = "eleven_multilingual_v2"
VOICE_STABILITY    = 0.5
VOICE_SIMILARITY   = 0.75

# --- Video Settings ---
VIDEO_WIDTH   = 1080
VIDEO_HEIGHT  = 1920   # Vertical 9:16 for Shorts
VIDEO_FPS     = 30
VIDEO_DURATION = 45    # seconds per Short

# --- Channel Settings ---
CHANNEL_NICHE    = "cute cats"
AFFILIATE_LINK   = "https://shopee.sg/yourlink"   # Your Shopee/Lazada affiliate link
CHANNEL_LANGUAGE = "bilingual"  # "english" | "chinese" | "bilingual"

# --- Pexels Search Queries (rotated per video) ---
PEXELS_QUERIES = [
    "cute cat playing",
    "kitten funny",
    "cat litter box",
    "cat toys",
    "fluffy cat",
    "cat grooming",
    "cat sleeping cute",
    "cat and owner"
]

# --- Output Paths ---
OUTPUT_SCRIPTS  = "output/scripts"
OUTPUT_AUDIO    = "output/audio"
OUTPUT_FOOTAGE  = "output/footage"
OUTPUT_VIDEOS   = "output/videos"
LOG_FILE        = "logs/run.log"

# --- Local binaries ---
FFMPEG_BIN      = "tools/ffmpeg/ffmpeg"
FFPROBE_BIN     = "tools/ffmpeg/ffprobe"

# --- YouTube Upload Defaults ---
YT_CATEGORY_ID  = "15"   # Pets & Animals
YT_PRIVACY      = "private"   # "public" | "private" | "unlisted"
YT_TAGS = [
    "cute cats", "cat shorts", "猫咪日常", "可爱猫咪",
    "cat litter", "猫砂", "cat toys", "cat care",
    "kitten", "funny cats", "cat facts"
]
