import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("spreman")


@bot.event
async def on_member_join(member):
    await member.send(f"welcome to the server")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("!"):
        await bot.process_commands(message)
        return

    if "kurac" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} - nemoj da psujes")

    await bot.process_commands(message)


@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name="tata")
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned a {role} role")
    else:
        await ctx.send(f"role doesnt exist")


@bot.command()
async def hello(ctx):
    await ctx.send(f"de si {ctx.author.mention} silo nebeska")


@bot.command()
async def unassign(ctx):
    role = discord.utils.get(ctx.guild.roles, name="tata")
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} is now no longer {role}")
    else:
        await ctx.send("role doesnt exist")

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(msg)

@bot.command()
async def reply(ctx):
    await ctx.reply("replying")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="new poll", description=question)
    await ctx.send(question, embed=embed)

@bot.command()
@commands.has_role("tata")
async def secret(ctx):
    await ctx.send("dobrodosao u klub super zloca")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f"nije ovo za tebe {ctx.author.mention}")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)