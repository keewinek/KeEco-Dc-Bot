import os

import asyncio

import discord
from discord import app_commands

from dotenv import load_dotenv

from discord.ext import commands
from discord.ext import tasks
from discord.ext import *

from discord.ext.commands import has_permissions

import economy
import database
import jobs
import schools
import other_jobs

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

    await bot.change_presence(activity=discord.Game(name="/work"))

    for guild in bot.guilds:
        await economy.update_all_guild_nicknames(guild)

@tasks.loop(minutes=15.0)
async def background_nick_update_loop():
    for guild in bot.guilds:
        await economy.update_all_guild_nicknames(guild)

@bot.tree.command(name="ping", description="Replies with Pong! (check if the bot is online)")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@bot.tree.command(name="reset_data", description="⚠️ Resets all your data (ex. balance will be 0)")
async def reset_data(interaction: discord.Interaction):
    secret_code = str(interaction.user.id)[0:6]
    await interaction.response.send_message(f"# This will reset all your KeEco data.\n⚠️ *Type `/reset_data_confirm {secret_code}`* (not recommended)⚠️", ephemeral=True)

@bot.tree.command(name="reset_data_confirm", description="⚠️ Confirm data reset.")
async def reset_data_confirm(interaction: discord.Interaction, secret_code: str):
    secret_code_valid = str(interaction.user.id)[0:6]

    if secret_code_valid == secret_code:
        economy.reset_user_data(interaction.user)
        await interaction.response.send_message("✅ Data reset successfully!")
    else:
        await interaction.response.send_message("❌ Invalid secret code!")
        return

@bot.tree.command(name="jobs", description="Displays all jobs in game.")
async def jobs_display(interaction: discord.Interaction):
    await interaction.response.send_message(embed=jobs.get_jobs_list_embed(interaction.user))

@bot.tree.command(name="schools", description="Displays all schools in game.")
async def schools_display(interaction: discord.Interaction):
    await interaction.response.send_message(embed=schools.get_schools_list_embed(interaction.user))

@bot.tree.command(name="fish", description="Go fishing.")
@app_commands.describe(equipment="Choose your fishing equipment. (Better equipment, better results.)")
@app_commands.choices(equipment=other_jobs.get_fishing_equipment_choices())
async def fish(interaction: discord.Interaction, equipment: int):
    await interaction.response.send_message(embed=other_jobs.fishing(interaction.user, equipment))
    await economy.update_user_nickname(interaction.user)

@bot.tree.command(name="walk_a_dog", description="Walk someone's dog and earn some money.")
async def walk_a_dog(interaction: discord.Interaction):
    await interaction.response.send_message(embed=other_jobs.walk_dog(interaction.user))
    await economy.update_user_nickname(interaction.user)

@bot.tree.command(name="job_quit", description="Quit your job.")
async def job_quit(interaction: discord.Interaction):
    if database.get_value(f"{interaction.user.id}_job", "") == "":
        await interaction.response.send_message("❌ You don't have a job to quit!")
        return

    await interaction.response.send_message(content=jobs.quit_current_job(interaction.user))

@bot.tree.command(name="job", description="Check your job.")
async def job(interaction: discord.Interaction):
    if database.get_value(f"{interaction.user.id}_job", "") == "":
        await interaction.response.send_message("❌ You don't have a job! Get one by using `/job_apply` command.")
        return

    await interaction.response.send_message(embed=jobs.get_job_embed(interaction.user))
    await economy.update_user_nickname(interaction.user)

@bot.tree.command(name="work", description="Work in your job.")
async def work(interaction: discord.Interaction):
    await interaction.response.send_message(content=jobs.work(interaction.user))
    await economy.update_user_nickname(interaction.user)

@bot.tree.command(name="job_apply", description="Apply for a job.")
@app_commands.describe(job="The name of the job you want to apply for.")
@app_commands.choices(job=jobs.get_job_choices())
async def job_apply(interaction: discord.Interaction, job: str):
    chosen_job = jobs.get_job(job)
    if chosen_job is None:
        await interaction.response.send_message("Job not found!", ephemeral=True)
        return
    
    await interaction.response.send_message(f"Applying for *{chosen_job.name}*...")
    await economy.update_user_nickname(interaction.user)

    msg = await interaction.original_response()

    await asyncio.sleep(2)
    await msg.edit(content = "Waiting for company response...")
    await asyncio.sleep(2)

    application_embed = jobs.send_job_application(chosen_job, interaction.user)

    await msg.edit(embed = application_embed, content = None)

@bot.tree.command(name="learn", description="Learn something new and gain 📖.")
@app_commands.describe(school="The name of the school you want to learn from.")
@app_commands.choices(school=schools.get_school_choices())
async def learn(interaction: discord.Interaction, school: str):
    chosen_school = schools.get_school(school)
    if chosen_school is None:
        await interaction.response.send_message("School not found!", ephemeral=True)
        return

    await interaction.response.send_message(content=schools.learn(interaction.user, chosen_school))

@bot.tree.command(name="bal", description="Check your balance")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"**Your balance:** `{economy.get_balance(interaction.user)} 💵` {interaction.user.mention}")
    await economy.update_user_nickname(interaction.user)

@bot.tree.command(name="stats", description="Check your balance")
async def ping(interaction: discord.Interaction):
    await economy.update_user_nickname(interaction.user)
    await interaction.response.send_message(embed=economy.get_user_stats_embed(interaction.user))

bot.run(TOKEN)