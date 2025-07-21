import discord
from discord.ext import commands
from datetime import datetime
import pytz
import os

# Load token from environment variable
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Time zones and their labels
timezones = {
    "🇺🇸 America": [
        ("🧊 Pacific (UTC-8)", "US/Pacific"),
        ("⛰️ Mountain (UTC-7)", "US/Mountain"),
        ("🟨 Central (UTC-6)", "US/Central"),
        ("🧃 Eastern (UTC-5)", "US/Eastern")
    ],
    "🇪🇺 Europe": [
        ("📦 Western (UTC 0)", "Etc/GMT"),
        ("🧀 Central (UTC+1)", "Europe/Paris"),
        ("🧊 Eastern (UTC+2)", "Europe/Kiev")
    ],
    "🌏 Asia-Pacific": [
        ("🍥 SEA/Manila (UTC+8)", "Asia/Manila"),
        ("🎯 Korea/Japan (UTC+9)", "Asia/Tokyo"),
        ("💧 ANZ/Oceania (UTC+10/+11)", "Australia/Sydney")
    ]
}

@bot.command(name="time")
async def show_timezones(ctx):
    now = datetime.now(pytz.UTC)  # Use aware datetime in UTC
    msg = "🕒 **Current Times:**\n\n"

    for region, zones in timezones.items():
        msg += f"{region}\n"
        for label, tz_str in zones:
            tz = pytz.timezone(tz_str)
            local_time = now.astimezone(tz)
            formatted = local_time.strftime("%I:%M %p")
            # Remove leading zero from hour only
            if formatted.startswith("0"):
                formatted = formatted[1:]
            msg += f"{label}: {formatted}\n"
        msg += "\n"

    await ctx.send(msg)

from keep_alive import keep_alive

keep_alive()

bot.run(TOKEN)
