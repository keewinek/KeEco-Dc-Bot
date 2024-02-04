import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

import database

async def update_user_nickname(member):
    try:
        job_emote = get_job(member)

        if job_emote != "":
            job_emote = job_emote[0]
        
        new_nick = f"{member.global_name} {job_emote}    ( {get_balance(member)} 💵 )"

        if member.nick == new_nick or member == member.guild.owner or get_balance(member) == 0:
            return

        await member.edit(nick=new_nick)
    except Exception as e:
        print(e)

def reset_user_data(user):
    database.set_value(f"{user.id}_balance", 0)
    database.set_value(f"{user.id}_experience", 0)
    database.set_value(f"{user.id}_education_level", 0)
    database.set_value(f"{user.id}_job", "")

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

def add_balance(member, balance):
    database.set_value(f"{member.id}_balance", get_balance(member) + balance)
    return balance

def get_balance(member):
    return int(database.get_value(f"{member.id}_balance", 0))

def get_experience(member):
    return int(database.get_value(f"{member.id}_experience", 0))

def get_job(member):
    return database.get_value(f"{member.id}_job", "")

def get_education_level(member):
    return int(database.get_value(f"{member.id}_education_level", 0))