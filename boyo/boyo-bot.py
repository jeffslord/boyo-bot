import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import boyo.utils as utils

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_SERVER")
# EXCLUDED_CHANNELS("845849148141862948")

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f"{bot.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )


@bot.command(name="boyo-bot")
async def fk(ctx):
    await ctx.send("fuck off")


@bot.command(name="boyo")
async def boyo(ctx, *args):
    try:
        text = utils.get_string_after_command(args)
        long_text = utils.text_generator(text)
        await ctx.reply(long_text)
    except Exception as e:
        print(e)
        await ctx.reply("fuck off")


@bot.command(name="boyo-short")
async def boyo_short(ctx, *args):
    try:
        text = utils.get_string_after_command(args)
        long_text = utils.text_generator(text)
        short_text = utils.text_summary(long_text)
        await ctx.reply(short_text)
    except Exception as e:
        print(e)
        await ctx.reply("fuck off")


@bot.command(name="pick")
async def pick(ctx, *args):
    print(args)
    res = random.choice(args)
    try:
        await ctx.reply(res)
    except Exception as e:
        print(e)
        await ctx.reply("fuck off")


@bot.command(name="text-to-image")
async def text_to_image(ctx, *args):
    text = utils.get_string_after_command(args)
    try:
        res = utils.text_to_image(text)
        print(res)
    except Exception as e:
        print(e)


@bot.command(name="spongebobify")
async def spongebobify(ctx):
    try:
        if ctx.message.reference is not None:
            reply_to = ctx.message.reference
            msg = reply_to.content
            # msg = msg.split(" ", 1)[1]
            new = "".join(random.choice((str.upper, str.lower))(x) for x in msg)
            print(msg)
            print(new)
            await reply_to.reply(new)
    except Exception as e:
        print(e)
        ctx.send("fuck off")

@bot.command(name="announce")
async def announce(ctx, *args):
    try:
        if ctx.message.author.name != "Lottli":
            return
        text = utils.get_string_after_command(args)
        channel = bot.get_channel(867586030508834837)
        await channel.send(text)
    except Exeption as e:
        print(e)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # elif message.author.name == "Lottli":
    try:
        # text = utils.get_string_after_command(message.content)
        sentiment = utils.text_sentiment(message.content)[0]
        print(sentiment)
        if "negative" in sentiment.lower():
            await message.reply(
                "My advanced AI has detected negativity in your message. I hope you are well."
            )
    except Exception as e:
        print(e)
        message.send("fuck off")
    finally:
        await bot.process_commands(message)


bot.run(TOKEN)


# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return
#     if message.author.name == "Lottli":
#         # print("This is jeff")
#         if "What do you think about that boyo-bot?" in message.content:
#             print("Fuck you and your class.")
#             await message.channel.send("Fuck you and your class.")
