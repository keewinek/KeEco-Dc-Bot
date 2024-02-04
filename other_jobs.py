import database
import economy
import random

import discord
from discord import app_commands

fishes = ["Tuna", "Salmon", "Cod", "Tilapia", "Sardines", "Kingfish"]
dog_walking_profit_range = (2, 8)

# Fishing

def get_fishing_equipment_choices():
    choices = []

    choices.append(app_commands.Choice(name=f"🎒🎣 Starter equipment · 20 💵", value=20))
    choices.append(app_commands.Choice(name=f"🎒🎣 Basic equipment · 50 💵", value=50))
    choices.append(app_commands.Choice(name=f"🎒🎣 Amateur equipment · 70 💵", value=70))
    choices.append(app_commands.Choice(name=f"🎒🎣 Pro equipment · 100 💵", value=100))
    choices.append(app_commands.Choice(name=f"🎒🎣 Expert equipment · 300 💵", value=300))

    return choices

def fishing(user, cost):
    user_experience = economy.get_experience(user)
    user_balance = economy.get_balance(user)

    if user_balance < cost:
        return discord.Embed(title="❌ Not enough money!", description=f"You need {user_balance - cost} 💵 more to buy this equipment.")

    money_earned = random.randint(cost - (cost // 3), cost + (cost // 2))

    database.set_value(f"{user.id}_balance", user_balance + money_earned - cost)
    database.set_value(f"{user.id}_experience", user_experience + 1)

    embed = discord.Embed(title="Fishing 🎣 ", description=f"🐠   You have successfully caught a **{random.choice(fishes)}**!", color=0x73f6ff)
    embed.add_field(name="Money earned", value=f"**+ {money_earned} 💵**", inline=True)
    embed.add_field(name="Equipment cost", value=f"− {cost} 💵", inline=True)

    embed.set_footer(text=f"{user.name}'s balance:   {user_balance + money_earned - cost} 💵 (Profit: {(money_earned - cost)})")

    return embed

# Dog walking

def walk_dog(user):
    embed = discord.Embed(title="Dog walking 🐶", description=f"🐶   You have successfully walked someone's dog!", color=0xebc37f)
    
    money_earned = random.randint(dog_walking_profit_range[0], dog_walking_profit_range[1])
    economy.add_balance(user, money_earned)

    embed.add_field(name="Money earned", value=f"**+ {money_earned} 💵**", inline=True)
    embed.set_footer(text=f"{user.name}'s balance: {economy.get_balance(user)} 💵")

    return embed