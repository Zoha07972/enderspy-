# EnderSpy v 0.1

EnderSpy V0.1 is a **basic open-source Minecraft server monitoring tool** written in Python. It can be used to check server status and send updates via a Discord bot.

## 🧠 Features

- **Single‐server monitor** (one IP:PORT per guild)  
- **Live status embeds** with MOTD, player count, uptime, version  
- **Configurable update interval** via `.env`  
- **Buttons** for Desktop & Mobile connect URLs  
- **Slash commands**:  
  - `/setup` – register or update the target server & channel  
  - `/removesetup` – clear the registration and stop updates  
- **Pure file storage**: all data in `server_data.json`  
- **Time zone support** via `.env` 

---

## 📋 Requirements

- Python 3.9+  
- Discord bot token with **applications.commands** enabled  
- Libraries:
  ```bash
  pip install discord.py mcstatus python-dotenv pytz
---
## 💬 Usage
Invite the bot to your server with the proper scopes (`bot` + `applications.commands`).

In any text channel, run:

```bash
/setup ip:port channel:#status server_type:java
```
The bot will verify and post an embed with the server status.

 - The bot will update the same message every UPDATE_INTERVAL seconds (default is 10 seconds).

To stop updates:
```bash
/removesetup 
```
---
## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Zoha07972/enderspy-.git
cd enderspy-
```
### 2. Set up a virtual environment (optional but recommended)
```bash
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
.venv\Scripts\activate       # Windows
```
### 3. Install dependencies
```bash
pip install discord.py mcstatus python-dotenv pytz
```
### 4. Create a .env file
Paste this content in a .env file at the root of the project:
```bash
BOT_TOKEN=your_bot_TOKEN
TIMEZONE=Asia/Kolkata
DESKTOP_CONNECT_URL=https://tlauncher.org/
PHONE_CONNECT_URL=https://play.google.com/store/apps/details?id=com.mojang.minecraftpe&pcampaignid=web_share
UPDATE_INTERVAL=10
BOT_THUMBNAIL_URL=IMAGEURL
```
Replace your_bot_TOKEN with your actual Discord bot token.

🚀 How to Run
```bash
python main.py
```
Make sure the bot is added to your Discord server with appropriate permissions.

## 📝 License
This project is licensed under the MIT License. See ```LICENSE``` for details.

---

### Explanation of Fixes:
- Added correct code block formatting for commands (`bash` and `arduino` blocks).
- Clarified the instructions about the bot verifying and posting an embed.
- Ensured consistent Markdown formatting.

Feel free to add it to your `README.md`.
