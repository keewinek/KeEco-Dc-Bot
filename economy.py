import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

import database

async def update_user_nickname(member):
    try:
        new_nick = f"{member.global_name}      ( {get_balance(member)} 💵 )"

        if member.nick == new_nick or member == member.guild.owner:
            return

        await member.edit(nick=new_nick)
    except Exception as e:
        print(e)

def get_user_stats_embed(user):
    return discord.Embed(
        title=f"{user.name}'s stats",
        description=f"`{get_balance(user)} 💵` `{get_experience(user)} 🔮` `{get_education_level(user)} 📖`",
        color=discord.Color.green()
    )

async def update_all_guild_nicknames(guild):
    for member in guild.members:
        if member.bot:
            continue

        await update_user_nickname(member)

def get_balance(member):
    return int(database.get_value(f"{member.id}_balance", 0))

def get_experience(member):
    return int(database.get_value(f"{member.id}_experience", 0))

def get_education_level(member):
    return int(database.get_value(f"{member.id}_education_level", 0))