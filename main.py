import discord
from discord.ext import commands
from datetime import datetime
import pytz
import os

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

timezones = {
    "🇺🇸 America": [
        ("🧊 Pacific", "US/Pacific"),
        ("⛰️ Mountain", "US/Mountain"),
        ("🟨 Central", "US/Central"),
        ("🧃 Eastern", "US/Eastern")
    ],
    "🇪🇺 Europe": [
        ("📦 Western", "Etc/GMT"),
        ("🧀 Central", "Europe/Paris"),
        ("🧊 Eastern", "Europe/Kiev"),
        ("🇬🇧 UK (London)", "Europe/London")
    ],
    "🌏 Asia-Pacific": [
        ("🍥 SEA/Manila", "Asia/Manila"),
        ("🎯 Korea/Japan", "Asia/Tokyo"),
        ("💧 ANZ/Oceania", "Australia/Sydney")
    ],
    "🖥️ Game Servers": [
        ("🌴 Palmon Server", "Etc/GMT+2")
    ]
}

@bot.command(name="time")
async def show_timezones(ctx):
    now = datetime.now(pytz.UTC)
    msg = "🕒 **Current Times:**\n\n"

    for region, zones in timezones.items():
        msg += f"{region}\n"
        for label, tz_str in zones:
            tz = pytz.timezone(tz_str)
            local_time = now.astimezone(tz)

            offset_sec = local_time.utcoffset().total_seconds()
            hours_offset = int(offset_sec // 3600)
            minutes_offset = int((offset_sec % 3600) // 60)
            sign = '+' if hours_offset >= 0 else '-'
            offset_str = f"UTC{sign}{abs(hours_offset):02d}:{abs(minutes_offset):02d}"

            formatted_time = local_time.strftime("%I:%M %p").lstrip("0")
            msg += f"{label} ({offset_str}): {formatted_time}\n"
        msg += "\n"

    # Split if too long for Discord's 2000-char limit
    if len(msg) > 2000:
        for chunk in [msg[i:i+2000] for i in range(0, len(msg), 2000)]:
            await ctx.send(chunk)
    else:
        await ctx.send(msg)

from keep_alive import keep_alive
keep_alive()

bot.run(TOKEN)
