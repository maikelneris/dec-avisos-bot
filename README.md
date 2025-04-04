# Discord Bot

A simple Discord bot built with discord.py that responds to basic commands.

## Setup

1. Create a Discord Application and Bot:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application" and give it a name
   - Go to the "Bot" section and click "Add Bot"
   - Copy the bot token

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the bot:
   - Rename `.env.example` to `.env`
   - Replace `your_bot_token_here` with your actual bot token

4. Invite the bot to your server:
   - Go to OAuth2 > URL Generator in the Developer Portal
   - Select "bot" under scopes
   - Select the permissions you want to give the bot
   - Use the generated URL to invite the bot to your server

## Running the Bot

```bash
python bot.py
```

## Available Commands

- `!hello` - Bot responds with a friendly hello message
- `!ping` - Check bot's latency

## Requirements

- Python 3.8 or higher
- discord.py
- python-dotenv 