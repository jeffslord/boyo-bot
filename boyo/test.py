import openai
import logging
import os
import utils


# DEEPAI_API = os.getenv("DEEPAI_API", "")
# OPEN_API = os.getenv("OPEN_API", "")
# openai.api_key = OPEN_API
# try:
#     completion = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt="Boyo is a chatbot.\nOld Man Melcon:I really like bananas\nMatt:Oh really? I hate them.\nRyan:boyo what is your name?\nBoyo:",
#         max_tokens=1024,
#         n=1,
#         temperature=1.0,
#         stop=["\n"]
#     )
#     text_response = completion.choices[0].text
#     print(text_response)
# except Exception as e:
#     logging.info("Error during GPT generation, returning general response")
#     logging.error(e)
#     text_response = "I'm sorry, I don't feel like responding right now."
