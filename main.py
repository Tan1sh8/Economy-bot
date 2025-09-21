import discord
from discord.ext import commands
import json
import os

# Load config
with open("config.json") as f:
    config = json.load(f)

PREFIX = config.get("prefix", ".")
TOKEN = config.get("token")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Load cogs
bot.load_extension("cogs.economy")
bot.load_extension("cogs.admin")

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

bot.run(TOKEN)
