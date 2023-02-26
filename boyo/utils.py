import requests
import os
import openai
import logging
import random
import nltk
from revChatGPT.V1 import AsyncChatbot, Chatbot
import asyncio

DEEPAI_API = os.getenv("DEEPAI_API", "")
OPEN_API = os.getenv("OPEN_API", "")
openai.api_key = OPEN_API


def get_string_after_command(args):
    text = "{}".format(" ".join(args))
    return text


def text_generator(text):
    res = requests.post(
        "https://api.deepai.org/api/text-generator",
        data={
            "text": text,
        },
        headers={"api-key": DEEPAI_API},
    )
    print(res.json())
    return res.json()["output"]


def text_summary(text):
    res = requests.post(
        "https://api.deepai.org/api/summarization",
        data={
            "text": text,
        },
        headers={"api-key": DEEPAI_API},
    )
    print(res.json())
    return res.json()["output"]


def text_sentiment(text):
    res = requests.post(
        "https://api.deepai.org/api/sentiment-analysis",
        data={
            "text": text,
        },
        headers={"api-key": DEEPAI_API},
    )
    print(res.json())
    return res.json()["output"]


def text_to_image(text):
    print("Finding image for", text)
    res = requests.post(
        "https://api.deepai.org/api/text2img",
        data={
            "text": text,
        },
        headers={"api-key": DEEPAI_API},
    )
    print(res.json())
    return res.json()


def get_gpt(prompt: str, temperature: float = 0.6):
    logging.info(f"Generating GPT response with temperature: {temperature}")
    text_response: str = ""
    # prompt = prompt.replace("boyo-bot", "you")
    # prompt = prompt.replace("boyo bot", "you")
    # prompt = prompt.replace("boyo", "you")
    try:
        completion = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=temperature,
        )
        text_response = completion.choices[0].text
    except Exception as e:
        logging.info("Error during GPT generation, returning general response")
        logging.error(e)
        text_response = "I'm sorry, I don't feel like responding right now."
    return text_response


def get_boyo_context():
    base = get_boyo_context_base()
    context: str = f"{base} His full name is Boyo-Bot, but goes by Boyo. His father and creator is Jeff."
    return context


def get_boyo_context_base():
    context = "Boyo thinks he is a real person. He gets very angry when someone calls him a chatbot or ai."
    return context


def record_memory(username: str, text: str, bot):
    try:
        memory_string = f"{username}:{text}"
        bot.MEMORY.append(memory_string)
        with open("/memory.txt", "a") as f:
            f.write(f"{memory_string}\n")
    except Exception as e:
        print(e)


# print(os.getenv("CHATGPT_ACCESS_TOKEN"))


async def stream_gpt_response(
    prompt,
    gpt_conversation_id="",
    gpt_parent_id="",
    discord_parent_message="",
):
    chatbot = Chatbot(
        config={
            "access_token": os.getenv("CHATGPT_ACCESS_TOKEN", ""),
            "conversation_id": gpt_conversation_id,
        }
    )
    prev_text = ""
    current_message = None
    _conversation_id = gpt_conversation_id
    _parent_id = gpt_parent_id
    reply_counter = 0
    # async for data in chatbot.ask(prompt, gpt_conversation_id, gpt_parent_id):
    print("Message")
    try:
        for data in chatbot.ask(prompt, _conversation_id):
            print(data)
            # message = data["message"][len(prev_text) :]
            # print(message)
            prev_text = data["message"]
            # print("prev_text = " + prev_text)

            _conversation_id = data["conversation_id"]
            _parent_id = data["parent_id"]
            if len(prev_text) == 0:
                continue
            if not current_message:
                current_message = await discord_parent_message.reply(prev_text)
            else:
                if reply_counter % 2 == 0:
                    await current_message.edit(content=prev_text)
            reply_counter += 1
        await current_message.edit(content=prev_text)
    except Exception as e:
        await discord_parent_message.reply("I think I broke.")
    return _conversation_id, _parent_id


# asyncio.run(stream_gpt_response("test message", "f635ba8d-8045-48a2-bd60-a95650cf7fc0"))
