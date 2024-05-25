import openai
import os
from dotenv import load_dotenv

openai.api_key = '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'

def get_definition_gpt(word):
    prompt = f"Provide a concise definition for a term commonly used to refer to {word}, without explicitly mentioning the term in English. Keep it short and simple."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful chat assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message['content']