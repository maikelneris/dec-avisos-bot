import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime
import pytz
import logging
from logging.handlers import RotatingFileHandler

# Set up logging
logger = logging.getLogger('discord_bot')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('logs.txt', maxBytes=1024*1024, backupCount=5, encoding='utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Load environment variables
load_dotenv()

# Set up bot with command prefix '!'
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Enable member intents for user mentions
bot = commands.Bot(command_prefix='!', intents=intents)

def parse_avisos_file():
    """Parse the AVISOS.md file and return a list of message instructions"""
    messages = []
    try:
        with open('AVISOS.md', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):  # Skip empty lines and comments
                    try:
                        channel_id, days, times, message = line.split(';')
                        # Split days if multiple days are provided
                        days = [day.strip().lower() for day in days.split(',')]
                        # Split time if multiple times are provided
                        times = [t.strip() for t in times.split(',')]
                        messages.append({
                            'channel_id': int(channel_id.strip()),
                            'days': days,
                            'times': times,
                            'message': message
                        })
                    except ValueError as e:
                        logger.error(f"Invalid line format in AVISOS.md: {line} - Error: {str(e)}")
    except FileNotFoundError:
        logger.error("AVISOS.md file not found")
    return messages

def should_send_message(days, times):
    """Check if a message should be sent based on current day and time"""
    current_time = datetime.now(pytz.timezone('America/Cuiaba'))
    current_day = current_time.strftime('%a').lower()
    current_hour_min = current_time.strftime('%H:%M')
    
    return current_day in days and current_hour_min in times

@tasks.loop(minutes=1)
async def check_messages():
    """Check and send scheduled messages every minute"""
    messages = parse_avisos_file()
    for msg in messages:
        if should_send_message(msg['days'], msg['times']):
            try:
                channel = bot.get_channel(msg['channel_id'])
                if not channel:
                    logger.error(f"Could not find channel with ID {msg['channel_id']}")
                    continue
                    
                # Process message to handle user mentions
                processed_message = msg['message']
                if '@' in processed_message:
                    # Get all members in the guild
                    guild = channel.guild
                    members = guild.members
                    
                    # Replace @username with proper mention
                    for member in members:
                        if f'@{member.name}' in processed_message or f'@{member.display_name}' in processed_message:
                            processed_message = processed_message.replace(f'@{member.name}', member.mention)
                            processed_message = processed_message.replace(f'@{member.display_name}', member.mention)
                
                await channel.send(processed_message)
                logger.info(f"Sent message to channel {msg['channel_id']}: {processed_message}")
            except Exception as e:
                logger.error(f"Error sending message to channel {msg['channel_id']}: {e}")

@bot.event
async def on_ready():
    logger.info(f'Bot {bot.user} has connected to Discord!')
    # Log current time and timezone when bot starts
    current_time = datetime.now(pytz.timezone('America/Cuiaba'))
    logger.info(f'Bot started at: {current_time.strftime("%Y-%m-%d %H:%M:%S %Z")}')
    check_messages.start()

@bot.event
async def on_error(event, *args, **kwargs):
    logger.error(f'Error in {event}:', exc_info=True)

@bot.command(name='hello')
async def hello(ctx):
    """Responds with a friendly hello message"""
    await ctx.send(f'Hello {ctx.author.name}! 👋')
    logger.info(f'Sent hello message to {ctx.author.name}')

@bot.command(name='ping')
async def ping(ctx):
    """Check bot's latency"""
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! Latency: {latency}ms')
    logger.info(f'Ping command used by {ctx.author.name}. Latency: {latency}ms')

@bot.command(name='channel_id')
async def channel_id(ctx):
    """Shows the ID of the current channel"""
    await ctx.send(f'This channel\'s ID is: `{ctx.channel.id}`\nYou can use this ID in your AVISOS.md file.')
    logger.info(f'Channel ID requested by {ctx.author.name} for channel {ctx.channel.name}')

@bot.command(name='user_id')
async def user_id(ctx, member: discord.Member = None):
    """Shows the ID of a user (or yourself if no user specified)"""
    if member is None:
        member = ctx.author
    await ctx.send(f'User {member.name}\'s ID is: `{member.id}`\nYou can use this ID to mention them in messages.')
    logger.info(f'User ID requested by {ctx.author.name} for user {member.name}')

@bot.command(name='time')
async def current_time(ctx):
    """Shows the current time being used by the bot"""
    current_time = datetime.now(pytz.timezone('America/Cuiaba'))
    await ctx.send(f'Current bot time: {current_time.strftime("%Y-%m-%d %H:%M:%S %Z")}')
    logger.info(f'Time check requested by {ctx.author.name}')

@bot.command(name='check_schedule')
async def check_schedule(ctx):
    """Check current scheduled messages"""
    messages = parse_avisos_file()
    if not messages:
        await ctx.send("No messages scheduled.")
        logger.info("Schedule check: No messages found")
        return
        
    response = "**Scheduled Messages:**\n"
    for i, msg in enumerate(messages, 1):
        response += f"{i}. Channel: {msg['channel_id']} | Days: {', '.join(msg['days'])} | Times: {', '.join(msg['times'])} | Message: {msg['message']}\n"
    
    await ctx.send(response)
    logger.info(f'Schedule check requested by {ctx.author.name}')

@bot.command(name='logs')
@commands.has_permissions(administrator=True)
async def show_logs(ctx, lines: int = 10):
    """Shows the last X lines of the log file (admin only)"""
    try:
        with open('logs.txt', 'r', encoding='utf-8') as file:
            logs = file.readlines()
            last_logs = logs[-lines:] if len(logs) > lines else logs
            log_content = ''.join(last_logs)
            if len(log_content) > 1900:  # Discord message limit is 2000 characters
                log_content = log_content[-1900:]
            await ctx.send(f'```\n{log_content}\n```')
            logger.info(f'Logs requested by admin {ctx.author.name}')
    except Exception as e:
        await ctx.send(f'Error reading logs: {str(e)}')
        logger.error(f'Error showing logs: {e}')

# Run the bot
try:
    bot.run(os.getenv('DISCORD_TOKEN'))
except Exception as e:
    logger.critical(f'Failed to start bot: {e}') 