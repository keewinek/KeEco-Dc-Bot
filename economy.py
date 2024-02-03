import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

async def update_user_nickname(member):
    await member.edit(nick=f"{member.name} | test")

async def update_all_guild_nicknames(guild):
    for member in guild.members:
        if member.bot:
            continue

        await member.edit(nick="Bruh")