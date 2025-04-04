# Discord Bot

A simple Discord bot built with discord.py that sends scheduled messages and responds to commands.

## Features

- Scheduled message sending based on day and time
- Timezone support (Cuiabá/MT)
- Rotating log system
- Admin commands for monitoring
- Auto-restart capability when running as a Windows service

## Setup

1. Create a Discord Application and Bot:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application" and give it a name
   - Go to the "Bot" section and click "Add Bot"
   - Under "Privileged Gateway Intents", enable "Message Content Intent"
   - Copy the bot token

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the bot:
   - Rename `.env.example` to `.env`
   - Replace `your_bot_token_here` with your actual bot token
   - Add your channel ID (use !channel_id command to get it)

4. Invite the bot to your server:
   - Go to OAuth2 > URL Generator in the Developer Portal
   - Select "bot" under scopes
   - Select the following permissions:
     - Read Messages/View Channels
     - Send Messages
     - Read Message History
   - Use the generated URL to invite the bot to your server

## Message Scheduling

Messages are scheduled using the `AVISOS.md` file. Each line follows this format:
```
day1,day2;time1,time2;message
```

Example:
```
mon,wed;14:30;Good afternoon everyone!
fri;09:00,15:00;Weekend is coming!
```

- Days can be: mon, tue, wed, thu, fri, sat, sun
- Times should be in 24-hour format (HH:MM)
- Multiple days or times should be separated by commas
- Fields are separated by semicolons

## Available Commands

- `!hello` - Bot responds with a friendly hello message
- `!ping` - Check bot's latency
- `!time` - Shows the current bot time (Cuiabá timezone)
- `!channel_id` - Shows the ID of the current channel
- `!check_schedule` - Lists all scheduled messages
- `!logs [number]` - Shows last X lines of logs (admin only, default 10 lines)

## Running the Bot

### Manual Start
```bash
python bot.py
```

### Auto-start with Windows

1. Open Task Scheduler (Windows + R, type `taskschd.msc`)
2. Create Basic Task:
   - Name: "Discord Bot"
   - Trigger: "When the computer starts"
   - Action: "Start a program"
   - Program: Select `start_bot.bat`
   - Start in: Your bot's directory path

3. Modify Task Settings:
   - Right-click task → Properties
   - Conditions tab:
     - Uncheck "Stop if computer switches to battery power"
   - Settings tab:
     - Check "Run task as soon as possible after scheduled start is missed"
     - Check "If task fails, restart every: 1 minute"
     - Set "Attempt to restart up to: 3 times"

## Logging

The bot maintains logs in `logs.txt` with the following features:
- Rotates when file reaches 1MB
- Keeps 5 backup files
- Logs include timestamp, level, and message
- View logs through Discord using `!logs` command (admin only)

## Requirements

- Python 3.8 or higher
- discord.py
- python-dotenv
- pytz

## File Structure

- `bot.py` - Main bot code
- `AVISOS.md` - Message schedule configuration
- `.env` - Bot configuration and tokens
- `logs.txt` - Log file (auto-generated)
- `start_bot.bat` - Windows startup script

## Troubleshooting

1. If the bot doesn't start:
   - Check if the token in `.env` is correct
   - Verify that CHANNEL_ID is set correctly
   - Check `logs.txt` for error messages

2. If scheduled messages aren't sending:
   - Verify the format in `AVISOS.md`
   - Check if the bot has permissions in the channel
   - Use `!time` to verify the bot's current time
   - Use `!check_schedule` to verify your scheduled messages

3. If the bot goes offline:
   - Check your internet connection
   - Verify the Task Scheduler settings
   - Review `logs.txt` for any errors 