from openai import OpenAI
import os
from dotenv import load_dotenv
from prompt import prompt

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def request_content(text):
    user_prompt = prompt["summarize"]
    code = None

    completion = client.chat.completions.create(
        messages = [
            # {
            #     "role": "system",
            #     "content": user_prompt.format(text=text)
            # },
            {
                "role": "user",
                "content": user_prompt.format(text=text)
            }
        ],
        model="gpt-4o-mini",
        # response_format={"type": "json_object"},
    )

    return completion.choices[0].message.content

#text = ''
#print(request_content(text))