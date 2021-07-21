import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
import random

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_SERVER")

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


# @client.event
# async def on_ready():
#     print(f"{client.user} has connected to Discord!")
#     guild = discord.utils.get(client.guilds, name=GUILD)
#     print(
#         f"{client.user} is connected to the following guild:\n"
#         f"{guild.name}(id: {guild.id})"
#     )
#     role_name = "Boyo"
#     for m in guild.members:
#         await m.add_roles(discord.utils.get(m.guild.roles, name=role_name))
#         print(m)


bot = commands.Bot(command_prefix="!")


@bot.command(name="boyo-bot")
async def fk(ctx):
    await ctx.send("fuck off")


@bot.command(name="boyo")
async def test(ctx, *args):
    text = "{}".format(" ".join(args))
    r = requests.post(
        "https://api.deepai.org/api/text-generator",
        data={
            "text": text,
        },
        headers={"api-key": "9cbf150a-3ac2-40f6-8a44-3a984f8fe3af"},
    )
    print(r.json())
    try:
        await ctx.send(r.json()["output"])
    except Exception as e:
        print(e)
        await ctx.send("fuck off")


@bot.command(name="pick")
async def pick(ctx, *args):
    print(args)
    res = random.choice(args)
    try:
        await ctx.send(res)
    except Exception as e:
        print(e)
        await ctx.send("fuck off")


# client.run(TOKEN)
bot.run(TOKEN)
