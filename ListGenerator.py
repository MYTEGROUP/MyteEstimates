#ListGenerator.py
from openai import OpenAI
import os
from dotenv import load_dotenv


# Load environment variables from the project directory
load_dotenv('credentials.env')
api_key = os.getenv('OPENAI_API_KEY')

openai_client = OpenAI(api_key=api_key)



# Function to generate text using OpenAI API
def generate_list(system_context, assistant_context, initial_prompt):
    response = openai_client.chat.completions.create(
        model="gpt-4-1106-preview",
        temperature=0.2,
        max_tokens=3000,
        messages=[
            {"role": "system", "content": system_context},
            {"role": "assistant", "content": assistant_context},
            {"role": "user", "content": initial_prompt}
        ]
    )
    return response.choices[0].message.content
