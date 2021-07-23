import requests
import os

DEEPAI_API = os.getenv("DEEPAI_API")


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
