import os

import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

import economy

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="ping", description="Replies with Pong! (check if the bot is online)")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@bot.tree.command(name="bal", description="Check your balance")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Your balance: 0 💵")

bot.run(TOKEN)