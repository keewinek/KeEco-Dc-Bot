import discord
import database
from discord import app_commands
import random

class School:
    def __init__(self, name, cost, learning_points_gain):
        self.name = name
        self.cost = cost
        self.learning_points_gain = learning_points_gain

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

all_schools = [
    School("🏫 Public School", 20, 1),
    School("🏫 Social School No. 62", 31, 2),
    School("🏫 Social School No. 24", 45, 5),
    School("🏫 Social School No. 1", 52, 15),
    School("🏫 Private School No. 478", 75, 40),
    School("🏫 Private School No. 679", 100, 72),
    School("🏫 Private School No. 123", 200, 152),
    School("🏫 Luxury School", 17000, 1000),
]

def get_schools_list_embed(user):
    user_balance = int(database.get_value(f"{user.id}_balance", 0))

    embed = discord.Embed(title="🏫   Schools list:", description="Use `/learn [School title]` to learn in that school.\n*--------*", color=0xe0a15e)

    for school in all_schools:
        field_value += f" • **Cost**: {school.cost} 💵\n"
        field_value += f" • **Education level**: {school.learning_points_gain} 📖\n"
        field_value += f"*--------*\n"

        embed.add_field(name=f"{school.name}", value=field_value, inline=False)

    embed.set_footer(text=f"{user.name}'s balance: {user_balance} 💵")
    
    return embed

def get_school(name):
    for school in all_schools:
        if school.name == name:
            return school

    return None

def learn(user, school):
    user_balance = int(database.get_value(f"{user.id}_balance", 0))
    user_education_level = int(database.get_value(f"{user.id}_education_level", 0))

    if user_balance < school.cost:
        return f"❌ You don't have enough money to learn in that school! You need {school.cost - user_balance} 💵 more."

    database.set_value(f"{user.id}_balance", user_balance - school.cost)
    database.set_value(f"{user.id}_education_level", user_education_level + school.learning_points_gain)

    return f"✅ You have successfully learned in **{school.name}** and earned {school.learning_points_gain} 📖."

def get_school_choices():
    choices = []

    schools_to_show = all_schools
    schools_to_show.reverse()

    for school in schools_to_show:
        spaces_to_add = 4
        choices.append(app_commands.Choice(name=f"{school.name} {((spaces_to_add) * '  ')}· {school.cost} 💵 · {school.learning_points_gain} 📖", value=school.name))

    return choices