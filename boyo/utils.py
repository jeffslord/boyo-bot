import requests
import os
import openai
import logging
import random

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
    prompt = prompt.replace("boyo-bot", "you")
    prompt = prompt.replace("boyo bot", "you")
    prompt = prompt.replace("boyo", "you")
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


def embellish_gpt_prompt(prompt: str, author_display_name: str):
    thank_author: bool = random.choices([True, False], weights=[3, 7])[0]
    ignore_question: bool = random.choices([True, False], weights=[1, 19])[0]
    hate_response: bool = random.choices([True, False], weights=[1, 10])[0]
    built_prompt: str = ""

    if ignore_question:
        built_prompt = "reply saying you don't feel like talking to them"
        return built_prompt

    if thank_author:
        built_prompt = f"Thank {author_display_name} for talking to you. Then "
    built_prompt = f'Reply to: "{prompt}"'
    if hate_response:
        built_prompt = f"{built_prompt}. Reply like you hate me."

    return built_prompt
