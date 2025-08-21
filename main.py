import discord
from discord.ext import commands
from datetime import datetime
from zoneinfo import ZoneInfo
import os

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN environment variable is not set.")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# All entries below are DST-aware where applicable (city-based zones).
timezones = {
    "🇺🇸 America": [
        ("🧊 Pacific", "America/Los_Angeles"),
        ("⛰️ Mountain", "America/Denver"),
        ("🟨 Central", "America/Chicago"),
        ("🧃 Eastern", "America/New_York"),
    ],
    "🇪🇺 Europe": [
        ("📦 Western (Lisbon)", "Europe/Lisbon"),        # Portugal/Canaries with DST
        ("🧀 Central (Amsterdam)", "Europe/Amsterdam"),  # NL/DE/FR/BE/ES(continental) with DST
        ("🧊 Eastern (Kyiv)", "Europe/Kiev"),            # EET/EEST (use Europe/Kyiv if your system supports it)
        ("🇬🇧 UK (London)", "Europe/London"),            # GMT/BST auto
    ],
    "🌏 Asia-Pacific": [
        ("🍥 SEA/Manila", "Asia/Manila"),
        ("🎯 Korea/Japan", "Asia/Tokyo"),
        ("💧 ANZ/Oceania", "Australia/Sydney"),
    ],
    "🖥️ Game Servers": [
        # Fixed offset (no DST). If this should follow a real region with DST, replace with a city zone.
        ("🌴 Palmon Server", "Etc/GMT+2"),
    ],
}

@bot.command(name="time")
async def show_timezones(ctx):
    now = datetime.now(tz=ZoneInfo("UTC"))
    msg = "🕒 **Current Times (DST-aware):**\n\n"

    for region, zones in timezones.items():
        msg += f"{region}\n"
        for label, tz_str