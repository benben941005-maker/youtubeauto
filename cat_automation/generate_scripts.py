"""
Module 1: generate_scripts.py
Uses Claude API to batch-generate bilingual cat Shorts scripts.
Output: JSON files in output/scripts/
"""

import anthropic
import json
import os
import re
from datetime import datetime
from config import CLAUDE_API_KEY, OUTPUT_SCRIPTS, AFFILIATE_LINK

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

SCRIPT_PROMPT = """You are a YouTube Shorts scriptwriter specializing in cute cat content.

Generate {count} YouTube Shorts scripts about cats. Each script should be exactly 40-45 seconds when read aloud.

STRICT FORMAT — return ONLY a valid JSON array, no other text:

[
  {{
    "id": 1,
    "topic": "cat litter tips",
    "hook_en": "Did you know most cat owners are making this mistake with litter?",
    "hook_zh": "你知道吗？大多数猫主人都在犯这个猫砂错误！",
    "script_en": "Full English script here. 3 facts + natural product mention + CTA. 40-45 seconds.",
    "script_zh": "完整中文脚本，3个有趣事实 + 自然提到产品 + 行动号召。40-45秒。",
    "subtitle_lines": [
      {{"en": "Did you know most cat owners...", "zh": "你知道吗？大多数猫主人..."}},
      {{"en": "Fact 1: Cats prefer unscented litter", "zh": "事实1：猫咪更喜欢无香猫砂"}},
      {{"en": "Fact 2: Change litter every 2 weeks", "zh": "事实2：每两周换一次猫砂"}},
      {{"en": "Fact 3: Box size matters a lot!", "zh": "事实3：猫砂盆大小很重要！"}},
      {{"en": "Link in bio for our top pick 👇", "zh": "简介里有我们的推荐链接 👇"}}
    ],
    "title_en": "3 Cat Litter Mistakes You're Making 😱",
    "title_zh": "3个你一直在犯的猫砂错误 😱",
    "description_en": "Most cat owners don't know these litter box secrets! Check our top cat litter recommendation: {affiliate}",
    "description_zh": "大多数猫主人不知道这些猫砂秘密！查看我们推荐的猫砂：{affiliate}",
    "tags": ["cat litter", "猫砂", "cat tips", "猫咪护理", "cute cats"]
  }}
]

Topics to cover (rotate through these):
- Cat litter mistakes and tips (猫砂)
- Cat toy recommendations (猫玩具)  
- Kitten daily routines (猫咪日常)
- Cat grooming secrets (猫咪梳毛)
- Cat food tips (猫粮知识)
- Why cats do funny things (猫咪行为)
- Cat health tips (猫咪健康)

IMPORTANT:
- Hook must be shocking/curiosity-inducing
- Naturally mention product (don't be salesy)
- End with CTA to check bio link
- Keep bilingual tone warm and fun
- Return ONLY the JSON array, nothing else
""".replace("{affiliate}", AFFILIATE_LINK)


def generate_scripts(count: int = 10) -> list[dict]:
    """Generate `count` scripts using Claude API."""
    print(f"🤖 Generating {count} scripts with Claude...")

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=8000,
        messages=[{
            "role": "user",
            "content": SCRIPT_PROMPT.format(count=count)
        }]
    )

    raw = response.content[0].text.strip()

    # Strip markdown code fences if present
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"```$", "", raw).strip()

    scripts = json.loads(raw)
    print(f"✅ Got {len(scripts)} scripts from Claude")
    return scripts


def save_scripts(scripts: list[dict]) -> str:
    """Save scripts to a dated JSON file."""
    os.makedirs(OUTPUT_SCRIPTS, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(OUTPUT_SCRIPTS, f"scripts_{timestamp}.json")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(scripts, f, ensure_ascii=False, indent=2)

    print(f"💾 Scripts saved to: {filepath}")
    return filepath


def load_latest_scripts() -> list[dict]:
    """Load the most recently generated scripts."""
    files = sorted([
        f for f in os.listdir(OUTPUT_SCRIPTS)
        if f.endswith(".json")
    ])
    if not files:
        raise FileNotFoundError("No scripts found. Run generate_scripts() first.")

    filepath = os.path.join(OUTPUT_SCRIPTS, files[-1])
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    scripts = generate_scripts(count=10)
    save_scripts(scripts)
    print(f"\n📋 Preview of Script #1:")
    print(f"  Title: {scripts[0]['title_en']}")
    print(f"  Hook:  {scripts[0]['hook_en']}")
