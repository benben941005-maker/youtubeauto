# 🐱 Cat YouTube Shorts Automation
### 全自动猫咪频道 | 从脚本到上传，一键完成

---

## 📁 Project Structure
```
cat_automation/
├── main.py              ← 主入口，一键运行全流程
├── config.py            ← 填入你的 API Keys
├── generate_scripts.py  ← Module 1: Claude 生成脚本
├── generate_voice.py    ← Module 2: ElevenLabs 配音
├── download_footage.py  ← Module 3: Pexels 下载素材
├── assemble_video.py    ← Module 4: FFmpeg 合成视频
├── upload_youtube.py    ← Module 5: 上传 YouTube
├── setup.bat            ← Windows 一键安装
├── requirements.txt
└── output/
    ├── scripts/         ← 生成的脚本 JSON
    ├── audio/           ← 配音 MP3 文件
    ├── footage/         ← 猫咪素材视频
    └── videos/          ← 最终成品 Short
```

---

## 🔑 Step 1: 获取所有 API Keys

### 1. Claude API Key (Anthropic)
- 前往：https://console.anthropic.com
- 注册账号 → API Keys → Create Key
- 免费额度：$5 试用金
- 填入 `config.py`: `CLAUDE_API_KEY = "sk-ant-..."`

### 2. ElevenLabs API Key (AI 配音)
- 前往：https://elevenlabs.io
- 注册免费账号 → Profile → API Key
- 免费额度：每月 10,000 字符（约 10 条视频）
- 填入 `config.py`: `ELEVENLABS_API_KEY = "..."`

### 3. Pexels API Key (免费素材)
- 前往：https://www.pexels.com/api
- 注册 → Get Started → 免费申请
- 完全免费，无限制
- 填入 `config.py`: `PEXELS_API_KEY = "..."`

### 4. YouTube Data API (上传视频)
这个步骤比较多，跟着做：

**Step A: 创建 Google Cloud 项目**
1. 前往 https://console.cloud.google.com
2. 创建新项目（随便命名，如 "CatChannel"）

**Step B: 启用 YouTube API**
1. 左侧菜单 → APIs & Services → Library
2. 搜索 "YouTube Data API v3" → Enable

**Step C: 创建 OAuth 凭证**
1. APIs & Services → Credentials
2. Create Credentials → OAuth client ID
3. Application type: **Desktop app**
4. 下载 JSON 文件
5. 重命名为 `client_secret.json`
6. 放到项目根目录

---

## 🚀 Step 2: 安装与运行

### Windows 安装
```bash
# 1. 双击运行 setup.bat
# 或在命令行：
pip install -r requirements.txt

# 安装 FFmpeg (选一种方式)
winget install ffmpeg
# 或从 https://ffmpeg.org/download.html 手动安装
```

### 运行顺序（建议先测试）

```bash
# 第一步：只生成脚本（不花钱，先测试）
python main.py --scripts-only

# 第二步：生成视频但不上传（检查质量）
python main.py --skip-upload --count 3

# 第三步：完整流程，3条视频
python main.py --count 3

# 第四步：正式批量生产，10条视频
python main.py --count 10
```

---

## 💰 Affiliate 设置

在 `config.py` 填入你的联盟链接：
```python
AFFILIATE_LINK = "https://shopee.sg/你的联盟链接"
```

**如何申请 Shopee/Lazada 联盟：**
- Shopee: https://affiliate.shopee.sg → 注册 → 获取推广链接
- Lazada: https://affiliate.lazada.com.sg → 同上
- 推荐产品：猫砂、猫玩具、猫粮、猫爬架

---

## ⏰ 自动每日运行 (Windows 任务计划)

```bash
# 在 Windows 任务计划程序中设置每天运行：
# 操作 → 程序: python
# 参数: C:\path\to\cat_automation\main.py --count 2
# 触发器: 每天 09:00
```

---

## 📊 预期收益时间线

| 月份 | 视频数 | 预期订阅 | 收入来源 |
|------|--------|----------|----------|
| 第1月 | 60条 | 100-300 | Affiliate 开始 |
| 第2月 | 120条 | 300-800 | Affiliate $50-200 |
| 第3月 | 180条 | 800-2000 | 申请 YPP |
| 第4月+ | 240条+ | 1000+ | AdSense + Affiliate |

---

## ❓ 常见问题

**Q: FFmpeg 找不到？**
A: 运行 `winget install ffmpeg`，然后重启命令行

**Q: ElevenLabs 免费额度用完了？**
A: 升级到 $5/月 的 Starter 计划（11万字符）

**Q: YouTube 上传失败？**
A: 删除 `youtube_token.pickle`，重新授权

**Q: 素材视频是否可以商用？**
A: Pexels 视频可以免费商用，无需注明来源

---

*Built with Claude + ElevenLabs + Pexels + FFmpeg + YouTube API*
