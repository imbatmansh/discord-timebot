import os
import discord
from discord.ext import commands
from datetime import datetime
from zoneinfo import ZoneInfo

# --- Token ---
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN environment variable is not set.")

# --- Intents ---
intents = discord.Intents.default()
intents.message_content = True  # make sure this is enabled in the bot portal too
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Timezones (DST-aware where applicable) ---
timezones = {
    "🇺🇸 America": [
        ("🧊 Pacific", "America/Los_Angeles"),
        ("⛰️ Mountain", "America/Denver"),
        ("🟨 Central", "America/Chicago"),
        ("🧃 Eastern", "America/New_York"),
    ],
    "🇪🇺 Europe": [
        ("📦 Western (Lisbon)", "Europe/Lisbon"),         # Portugal/Canaries with DST
        ("🧀 Central (Amsterdam)", "Europe/Amsterdam"),   # NL/DE/FR/BE/ES(continental) with DST
        ("🧊 Eastern (Kyiv)", "Europe/Kyiv"),             # modern tzdb name (not Europe/Kiev)
        ("🇬🇧 UK (London)", "Europe/London"),              # GMT/BST auto
    ],
    "🌏 Asia-Pacific": [
        ("🍥 SEA/Manila", "Asia/Manila"),
        ("🎯 Korea/Japan", "Asia/Tokyo"),
        ("💧 ANZ/Oceania", "Australia/Sydney"),
    ],
    "🖥️ Game Servers": [
        # Fixed offset (no DST). If Palmon should follow a real city/DST, swap to that city tz.
        ("🌴 Palmon Server", "Etc/GMT+2"),
    ],
}

def format_offset(dt):
    """Return 'UTC+HH:MM' or 'UTC-HH:MM' from a timezone-aware datetime."""
    offset = dt.utcoffset()
    if offset is None:
        return "UTC±00:00"
    total_seconds = int(offset.total_seconds())
    hours = total_seconds // 3600
    minutes = abs(total_seconds) % 3600 // 60
    sign = '+' if hours >= 0 else '-'
    return f"UTC{sign}{abs(hours):02d}:{minutes:02d}"

def format_time_12h(dt):
    """Return 12-hour time without a leading zero e.g. '9:05 PM'."""
    s = dt.strftime("%I:%M %p")
    return s[1:] if s.startswith("0") else s

@bot.command(name="time")
async def show_timezones(ctx):
    now_utc = datetime.now(tz=ZoneInfo("UTC"))
    msg = "🕒 **Current Times (DST-aware):**\n\n"

    for region, zones in timezones.items():
        msg += f"{region}\n"
        for label, tz_str in zones:
            try:
                tz = ZoneInfo(tz_str)
            except Exception:
                # Fallback if a tz name is missing on the host
                tz = ZoneInfo("UTC")
            local_time = now_utc.astimezone(tz)
            msg += f"{label} ({format_offset(local_time)}): {format_time_12h(local_time)}\n"
        msg += "\n"

    # Discord 2000-char safety
    if len(msg) > 2000:
        for i in range(0, len(msg), 2000):
            await ctx.send(msg[i:i+2000])
    else:
        await ctx.send(msg)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (id: {bot.user.id})")

# Optional keep_alive for Replit-style hosting
try:
    from keep_alive import keep_alive
    keep_alive()
except Exception:
    pass

bot.run(TOKEN)