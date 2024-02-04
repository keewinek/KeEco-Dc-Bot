import os

import asyncio

import discord
from discord import app_commands

from dotenv import load_dotenv

from discord.ext import commands
from discord.ext import tasks

from discord.ext.commands import has_permissions

import economy
import jobs

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

    for guild in bot.guilds:
        await economy.update_all_guild_nicknames(guild)

@tasks.loop(minutes=15.0)
async def background_nick_update_loop():
    for guild in bot.guilds:
        await economy.update_all_guild_nicknames(guild)

@bot.tree.command(name="ping", description="Replies with Pong! (check if the bot is online)")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@bot.tree.command(name="jobs", description="Displays all jobs in game.")
async def jobs_display(interaction: discord.Interaction):
    await interaction.response.send_message(embed=jobs.get_jobs_list_embed())

@bot.tree.command(name="job_apply", description="Apply for a job.")
@bot.tree.describe(job="The name of the job you want to apply for.")
@bot.tree.choices(job=jobs.get_job_choices())
async def job_apply(interaction: discord.Interaction, job: str):
    choosen_job = jobs.get_job(job)
    if choosen_job is None:
        await interaction.response.send_message("Job not found!", ephemeral=True)
        return
    
    await interaction.response.send_message(f"Applying for *{choosen_job.name}*...", ephemeral=True)

    await asyncio.sleep(1)

    application_embed = jobs.send_job_application(choosen_job, interaction.user)

    msg = await interaction.original_response()
    await msg.edit(embed = application_embed, content = None)

@bot.tree.command(name="bal", description="Check your balance")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"**Your balance:** `{economy.get_balance(interaction.user)} 💵` {interaction.user.mention}")
    await economy.update_user_nickname(interaction.user)

@bot.tree.command(name="update_all_nicknames", description="Update all server nicknames")
@commands.cooldown(1, 60, commands.BucketType.user)
@has_permissions(administrator=True)
async def update_all_nicknames(interaction: discord.Interaction):
    await interaction.response.send_message("Updating nicknames...", ephemeral = True)
    await economy.update_all_guild_nicknames(interaction.guild)

    msg = await interaction.original_response()
    await msg.edit(content="Nicknames updated!")

bot.run(TOKEN)