import requests
import os
import openai

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


def get_gpt(prompt: str):
    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.6,
    )
    text_response = completion.choices[0].text
    return text_response
