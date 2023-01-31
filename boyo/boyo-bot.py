import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import random
import boyo.utils as utils
from datetime import datetime, timedelta, time, timezone
import asyncio
import pytz


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN", "")
GUILD = os.getenv("DISCORD_SERVER", "")
# EXCLUDED_CHANNELS("845849148141862948")

intents = discord.Intents.all()
intents.members = True

# client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix="!", intents=intents)

bot.LAST_AUTO_REPLY_TIME = datetime.now() - timedelta(minutes=1)
bot.IS_RESPONDING = False

DAILY_TIME = time(18, 30, 0, 0, tzinfo=pytz.timezone("US/Eastern"))  # 6:30pm


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f"{bot.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )
    daily_question.start()


@bot.event
async def on_message(message):
    message_author = message.author
    message_author_display_name = message_author.display_name
    message_text = message.content
    if message.author == bot.user:
        print(f"Skipping request from: {str(message.author)}")
        return
    # elif "Lottli" in str(message.author.name):
    #     gpt_response = utils.get_gpt(message.content)
    #     await message.reply(gpt_response)
    else:
        if not bot.IS_RESPONDING:
            bot.IS_RESPONDING = True
            await asyncio.sleep(random.randint(2, 5))
            async with message.channel.typing():
                gpt_prompt: str = utils.embellish_gpt_prompt(
                    message_text, message_author_display_name
                )
                gpt_response = utils.get_gpt(gpt_prompt, random.random())
                await asyncio.sleep(random.randint(5, 10))
                bot.LAST_AUTO_REPLY_TIME = datetime.now()
                await message.reply(gpt_response)
            bot.IS_RESPONDING = False
    try:
        await bot.process_commands(message)
    except Exception as e:
        print(e)


@tasks.loop(time=DAILY_TIME)  # Create the task
async def daily_question():
    print("Sending daily message...")
    channel = bot.get_channel(392511448171020300)
    # channel = client.get_channel(392511448171020300)  # private general channel
    random_user = random.choice(channel.guild.members)
    gpt_prompt = f"say that you hope {random_user.display_name} had a good day, and then ask them a random thought provoking question."
    gpt_response = utils.get_gpt(gpt_prompt, random.random())
    response = f"{random_user.mention} {gpt_response}"
    await channel.send(response)


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


@bot.command(name="boyo-gpt")
async def boyo_gpt(ctx, *args):
    try:
        text = utils.get_string_after_command(args)
        print(f"Sending to gpt: {text}")
        gpt_response = utils.get_gpt(text)
        await ctx.reply(gpt_response)
    except Exception as e:
        print(e)
        await ctx.reply("Oops something went wrong.")


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
    except Exception as e:
        print(e)


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
