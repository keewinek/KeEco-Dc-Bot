import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

import database

async def update_user_nickname(member):
    try:
        new_nick = f"{member.display_name} | {get_balance(member)} 💵"

        if member.nick == new_nick:
            return

        await member.edit(nick=new_nick)
    except Exception as e:
        print(e)

async def update_all_guild_nicknames(guild):
    for member in guild.members:
        if member.bot:
            continue

        await update_user_nickname(member)

def get_balance(member):
    return int(database.get_value(f"member.id_balance", 0))