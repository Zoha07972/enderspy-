# -----------------------------------------------------------------------------
# File:        main.py
# Description: Main entrypoint that loads cogs and starts the Discord bot.
# Author:      X
# Created:     06/02/2025
# Updated:     12/05/2025
# -----------------------------------------------------------------------------

import os
import discord
from discord.ext import commands
import asyncio

import command.setup
import command.removesetup

# ---------------------------------------- Load Environment Variables ----------------------------------------
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Bot token not found in environment variables!")

# ---------------------------------- Bot Setup --------------------------------------
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

# ---------------------------------- Event Handlers ---------------------------------
@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    await bot.change_presence(activity=discord.Game(name="Minecraft"))
    print("Bot status set to 'Playing Minecraft'.")
    try:
        await setup_cogs()
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

# ---------------------------------- Command and Cog Setup --------------------------
async def setup_cogs():
    try:
        await command.setup.setup(bot)
        await command.removesetup.setup(bot)
        print("Core setup commands loaded successfully.")
    except Exception as e:
        print(f"Error loading cogs: {e}")

# ---------------------------------- Run the Bot ------------------------------------
bot.run(TOKEN)
