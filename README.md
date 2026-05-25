# 😈 Devil X Telegraph — Telegram File-to-URL Bot

A Telegram bot that converts images, videos, and audio files into **permanent direct links** by uploading to **5 hosting services simultaneously**.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0-green)](https://pyrogram.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## ✨ Features

- 📤 Upload files to **5 hosts at once** — Catbox, 0x0.st, Uguu.se, GoFile, Transfer.sh
- 🖼 Supports JPG, JPEG, PNG, GIF, MP4, MP3 and any document
- 📊 `/stats` command showing uploads by file type
- 👑 Owner-only `/users` and `/broadcast` commands
- 🔄 Supabase integration (optional — bot works fully without it)
- 🚀 Deploy anywhere: Termux, VPS, Railway, Render, Heroku, Koyeb, Docker, Replit

---

## 📋 Commands

| Command | Description | Access |
|---------|-------------|--------|
| `/start` | Welcome message & bot info | Everyone |
| `/help` | List all commands | Everyone |
| `/ping` | Check latency & uptime | Everyone |
| `/stats` | Upload counts by file type | Everyone |
| `/users` | View total users & chats | Owner only |
| `/broadcast` | Broadcast to all chats | Owner only |

---

## 🔑 Required Credentials

| Variable | Where to get it |
|----------|----------------|
| `BOT_TOKEN` | Message [@BotFather](https://t.me/BotFather) → `/newbot` |
| `API_ID` | [my.telegram.org/apps](https://my.telegram.org/apps) |
| `API_HASH` | [my.telegram.org/apps](https://my.telegram.org/apps) |
| `OWNER_ID` | Message [@userinfobot](https://t.me/userinfobot) → `/start` |

**Optional (for user tracking stats):**

| Variable | Where to get it |
|----------|----------------|
| `SUPABASE_URL` | [supabase.com](https://supabase.com) → Settings → API |
| `SUPABASE_KEY` | Same page, use the **service_role** key (not anon) |

---

## ☁️ Upload Hosts

| Host | Retention |
|------|-----------|
| 📦 [Catbox.moe](https://catbox.moe) | Permanent |
| 🔗 [0x0.st](https://0x0.st) | Long-term (size-based) |
| 🌐 [Uguu.se](https://uguu.se) | 48 hours |
| ☁️ [GoFile.io](https://gofile.io) | Permanent |
| 🚀 [Transfer.sh](https://transfer.sh) | 14 days |

---

## 🚀 Deployment Guides

---

### 📱 Termux (Android)

> No PC needed — run the bot directly from your phone.

**1. Install Termux**
Download from [F-Droid](https://f-droid.org/packages/com.termux/) (not Play Store).

**2. Install dependencies**
```bash
pkg update && pkg upgrade -y
pkg install python git -y
pip install --upgrade pip
```

**3. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/Devil_X_Telegraph.git
cd Devil_X_Telegraph
```

**4. Install Python packages**
```bash
pip install -r requirements.txt
```

**5. Create your `.env` file**
```bash
cp .env.example .env
nano .env
```
Fill in your credentials, then save (`Ctrl+X → Y → Enter`).

**6. Run the bot**
```bash
python3 -m DevilxTelegraph
```

**Keep it running after closing Termux:**
```bash
pkg install termux-services
sv-enable sshd
nohup python3 -m DevilxTelegraph &
```
Or use `screen`:
```bash
pkg install screen
screen -S bot
python3 -m DevilxTelegraph
# Detach: Ctrl+A then D
# Re-attach: screen -r bot
```

---

### 🐧 VPS / Linux (Ubuntu / Debian)

**1. Update system & install Python**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git screen -y
```

**2. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/Devil_X_Telegraph.git
cd Devil_X_Telegraph
```

**3. Install Python packages**
```bash
pip3 install -r requirements.txt
```

**4. Create your `.env` file**
```bash
cp .env.example .env
nano .env
```

**5. Run in background with screen**
```bash
screen -S devilbot
python3 -m DevilxTelegraph
# Detach: Ctrl+A then D
# Re-attach: screen -r devilbot
```

**Or run as a systemd service (auto-start on reboot):**
```bash
sudo nano /etc/systemd/system/devilbot.service
```
Paste:
```ini
[Unit]
Description=Devil X Telegraph Bot
After=network.target

[Service]
Type=simple
User=YOUR_LINUX_USER
WorkingDirectory=/home/YOUR_LINUX_USER/Devil_X_Telegraph
ExecStart=/usr/bin/python3 -m DevilxTelegraph
Restart=always
RestartSec=10
EnvironmentFile=/home/YOUR_LINUX_USER/Devil_X_Telegraph/.env

[Install]
WantedBy=multi-user.target
```
Then enable it:
```bash
sudo systemctl daemon-reload
sudo systemctl enable devilbot
sudo systemctl start devilbot
sudo systemctl status devilbot
```

---

### 🪟 Windows (Local)

**1. Install Python 3.11+**
Download from [python.org](https://www.python.org/downloads/) — check **"Add Python to PATH"** during install.

**2. Clone the repo**
```cmd
git clone https://github.com/YOUR_USERNAME/Devil_X_Telegraph.git
cd Devil_X_Telegraph
```

**3. Install packages**
```cmd
pip install -r requirements.txt
```

**4. Create your `.env` file**
Copy `.env.example` to `.env` and fill in your credentials using Notepad or VS Code.

**5. Run the bot**
Double-click `start.bat`, or from Command Prompt:
```cmd
python -m DevilxTelegraph
```

---

### 🚂 Railway (Free Tier Available)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app)

**1.** Push this repo to your GitHub account.

**2.** Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub**.

**3.** Select your repository.

**4.** Go to **Variables** tab and add:
```
BOT_TOKEN=your_bot_token
API_ID=your_api_id
API_HASH=your_api_hash
OWNER_ID=your_owner_id
```

**5.** Railway will auto-detect `railway.json` and deploy. Done!

> The `railway.json` in this repo is pre-configured.

---

### 🎨 Render (Free Tier Available)

**1.** Push this repo to your GitHub account.

**2.** Go to [render.com](https://render.com) → **New** → **Background Worker**.

**3.** Connect your GitHub repo.

**4.** Render will auto-detect `render.yaml`. Set the environment variables:
```
BOT_TOKEN=your_bot_token
API_ID=your_api_id
API_HASH=your_api_hash
OWNER_ID=your_owner_id
```

**5.** Click **Create Background Worker**. Done!

---

### 🔷 Heroku

**1.** Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

**2.** Login and create app:
```bash
heroku login
heroku create your-app-name
```

**3.** Set environment variables:
```bash
heroku config:set BOT_TOKEN=your_bot_token
heroku config:set API_ID=your_api_id
heroku config:set API_HASH=your_api_hash
heroku config:set OWNER_ID=your_owner_id
```

**4.** Add Python buildpack and deploy:
```bash
heroku buildpacks:set heroku/python
git push heroku main
```

**5.** Scale the worker:
```bash
heroku ps:scale worker=1
```

> The `Procfile` in this repo is pre-configured.

---

### ⚙️ Koyeb (Free Tier Available)

**1.** Go to [koyeb.com](https://koyeb.com) → **Create App** → **GitHub**.

**2.** Select your repository and branch.

**3.** Set environment variables:
```
BOT_TOKEN=your_bot_token
API_ID=your_api_id
API_HASH=your_api_hash
OWNER_ID=your_owner_id
```

**4.** Set the **Run command**:
```
python3 -m DevilxTelegraph
```

**5.** Deploy. Done!

> The `koyeb.yaml` in this repo is pre-configured.

---

### 🐳 Docker

**1.** Build the image:
```bash
docker build -t devil-x-telegraph .
```

**2.** Run the container:
```bash
docker run -d \
  --name devilbot \
  --restart always \
  -e BOT_TOKEN=your_bot_token \
  -e API_ID=your_api_id \
  -e API_HASH=your_api_hash \
  -e OWNER_ID=your_owner_id \
  devil-x-telegraph
```

**Or use a `.env` file with Docker:**
```bash
docker run -d --name devilbot --restart always --env-file .env devil-x-telegraph
```

**View logs:**
```bash
docker logs -f devilbot
```

---

### 🔄 Replit

**1.** Fork/import this repo on [replit.com](https://replit.com).

**2.** Go to **Secrets** tab (🔒 icon) and add:
```
BOT_TOKEN → your_bot_token
API_ID    → your_api_id
API_HASH  → your_api_hash
OWNER_ID  → your_owner_id
```

**3.** In Shell, run:
```bash
pip install -r requirements.txt
```

**4.** Set the run command to:
```bash
cd bot && python3 -m DevilxTelegraph
```

**5.** Click **Run**. Use [UptimeRobot](https://uptimerobot.com) to keep it alive 24/7.

---

## 📁 Project Structure

```
Devil_X_Telegraph/
├── Devil/                    # Plugin handlers (auto-loaded)
│   ├── __init__.py
│   ├── audio.py              # MP3 upload handler
│   ├── commands.py           # /ping, /stats, /users, /broadcast, /help
│   ├── handler_utils.py      # Shared upload logic
│   ├── jpg.py                # Photo upload handler
│   ├── mp4.py                # Video upload handler
│   ├── png.py                # Document upload handler
│   ├── start.py              # /start command
│   └── tracker.py            # User/chat tracking
├── DevilxTelegraph/
│   ├── __init__.py
│   └── __main__.py           # Bot entry point
├── auth.py                   # Load credentials from env
├── db.py                     # Supabase + in-memory stats
├── upload_helper.py          # Multi-host parallel uploader
├── requirements.txt
├── .env.example              # Template for credentials
├── Dockerfile                # Docker deployment
├── Procfile                  # Heroku deployment
├── railway.json              # Railway deployment
├── render.yaml               # Render deployment
├── koyeb.yaml                # Koyeb deployment
├── start.sh                  # Linux/VPS/Termux start script
└── start.bat                 # Windows start script
```

---

## 🗄️ Supabase Setup (Optional)

If you want user/chat tracking and `/users` stats to persist:

**1.** Create a free account at [supabase.com](https://supabase.com).

**2.** Create a new project.

**3.** Go to **SQL Editor** and run:
```sql
CREATE TABLE chats (
    chat_id BIGINT PRIMARY KEY,
    chat_type TEXT NOT NULL,
    title TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT NOW()
);
```

**4.** Go to **Settings → API** and copy:
- **Project URL** → `SUPABASE_URL`
- **service_role** key (not anon!) → `SUPABASE_KEY`

**5.** Add these to your `.env` or platform environment variables.

---

## ⚠️ Notes

- Files over **200 MB** are not supported by Telegram bots
- The session file (`DevilXTelegraph.session`) is created on first run — **keep it safe**
- If you move the bot to a new machine, copy the `.session` file too to avoid re-auth
- `/stats` counts resets when the bot restarts (in-memory only unless you add Supabase)
- Always run from the project root directory

---

## 👨‍💻 Credits

Created by [MR DEVIL](http://t.me/mrdevil12) — Join [Devil Bot's Channel](https://t.me/devilbots971) for updates.
