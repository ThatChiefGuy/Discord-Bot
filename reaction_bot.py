import discord
from discord.ext import commands
import logging
import dotenv
import os
import json


def dump_json(data, file, indent=4):
    with open(file, "w") as file:
        json.dump(data, file, indent=indent)

def load_json(file):
    with open(file, "r") as file:
        return json.load(file)


dotenv.load_dotenv()
token = os.getenv("DISCORD_TOKEN")

logging = logging.FileHandler("discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("redi")

@bot.event
async def on_reaction_add(reaction, user):
    data = load_json("roles.json")

    if user.bot:
        return

    if str(reaction.emoji) in list(data.keys()):
        role = discord.utils.get(reaction.message.guild.roles, name=data.get(str(reaction.emoji)))
        if role:
            await user.add_roles(role)
            await reaction.message.channel.send(f"{user.mention} reacted with {reaction.emoji} and is given {role} role")
        else:
            print("error acured")

@bot.event
async def on_reaction_remove(reaction, user):
    data = load_json("roles.json")

    if user.bot:
        pass

    if str(reaction.emoji) in list(data.keys()):
        role = discord.utils.get(reaction.message.guild.roles, name=data.get(str(reaction.emoji)))
        if role:
            await user.remove_roles(role)
            await reaction.message.channel.send(f"{user.mention} reacted with {reaction.emoji} and removed their {role} role")
        else:
            print("error accured")

@bot.command()
async def choose_role(ctx):
    data = load_json("roles.json")

    reactions = list(data.keys())
    message = await ctx.send("biraj svoj role sada!")
    for reaction in reactions:
        await message.add_reaction(reaction)

@bot.command()
async def define_role(ctx, role_name, new_icon):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        roles = load_json("roles.json")
        if role_name in roles.values():
            roles = {icon: role for icon, role in roles.items() if not role == role_name}
            roles.update({new_icon:role_name})
        else:
            roles.update({new_icon:role_name})

        dump_json(roles, "roles.json", indent=4)
    else:
        await ctx.channel.send("make sure to have the role before trying to assign an emoji to it")

@bot.command()
async def delete_role(ctx, role_name):
    roles = load_json("roles.json")
    if role_name in roles.values():
        roles = {icon: role for icon, role in roles.items() if not role == role_name}
        dump_json(roles, "roles.json", indent=4)
    else:
        await ctx.channel.send(f"role {role_name} is not defined for an emoji")


bot.run(token)