# textgen.py
import base64

from openai import OpenAI
import json
import os
import sys
import shutil
# Declare openai_client at the module level
openai_client = None
def get_base_path():
    """Determine and return the base path for application data."""
    if getattr(sys, 'frozen', False):
        # If running in a PyInstaller bundle
        return os.path.dirname(sys.executable)
    else:
        # If running in a normal Python environment (not bundled)
        # Use the directory two levels up from this file's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.abspath(os.path.join(current_dir, os.pardir))
        return base_path

def get_api_key():
    try:
        preferences_path = os.path.join(get_base_path(), 'storage', 'User_Preferences.json')

        with open(preferences_path, 'r') as file:
            preferences = json.load(file)
            return preferences.get('openai_api_key')
    except Exception as e:
        print(f"An error occurred while retrieving the API key: {e}")
        return None


def initialize_openai_client():
    global openai_client
    api_key = get_api_key()
    if api_key:
        openai_client = OpenAI(api_key=api_key)
    else:
        print("API key is not set. Please ensure the API key is correctly saved.")
        openai_client = None

def generate_text(system_context, assistant_context, initial_prompt):
    if not openai_client:
        initialize_openai_client()
    if not openai_client:
        # If the OpenAI client is not initialized, return a placeholder message or perform another fallback behavior
        return "OpenAI client is not initialized. Please set the OpenAI API key in User Preferences."

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            temperature=0.8,
            max_tokens=4000,
            messages=[
                {"role": "system", "content": system_context},
                {"role": "assistant", "content": assistant_context},
                {"role": "user", "content": initial_prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred while generating text: {e}")
        return f"An error occurred while generating text: {e} Please check the OpenAI API key and try again."
def generate_text_json(system_context, assistant_context, initial_prompt):
    initialize_openai_client()
    if not openai_client:
        # If the OpenAI client is not initialized, return a placeholder message or perform another fallback behavior
        return "OpenAI client is not initialized. Please set the OpenAI API key in User Preferences."

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        temperature=0.1,
        max_tokens=3000,
        response_format={ "type": "json_object"},
        messages=[
            {"role": "system", "content": system_context},
            {"role": "assistant", "content": assistant_context},
            {"role": "user", "content": initial_prompt}
        ]
    )
    return response.choices[0].message.content

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def vision_json(image_path, system_context, assistant_context, initial_prompt):
    initialize_openai_client()
    if not openai_client:
        return "OpenAI client is not initialized. Please set the OpenAI API key in User Preferences."

    base64_image = encode_image(image_path)

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,
        max_tokens=4096,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_context},
            {"role": "assistant", "content": assistant_context},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{initial_prompt}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ]
            }
        ]
    )
    return response.choices[0].message.content

def vision_text(image_path, system_context, assistant_context, initial_prompt):
    initialize_openai_client()
    if not openai_client:
        return "OpenAI client is not initialized. Please set the OpenAI API key in User Preferences."

    base64_image = encode_image(image_path)

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,
        max_tokens=4096,
        messages=[
            {"role": "system", "content": system_context},
            {"role": "assistant", "content": assistant_context},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{initial_prompt}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ]
            }
        ]
    )
    return response.choices[0].message.content


def text_to_speech(input_text, filename="question.mp3"):
    initialize_openai_client()
    if not openai_client:
        # If the OpenAI client is not initialized, return a placeholder message or perform another fallback behavior
        return "OpenAI client is not initialized. Please set the OpenAI API key in User Preferences."

    # Determine the base path of the application
    base_path = get_base_path()

    # Define the full path to the staticLinkedIN directory
    static_dir = os.path.join(base_path, 'staticLinkedIN')

    # Ensure the staticLinkedIN directory exists
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # Define the full path to the audio file within the staticLinkedIN directory
    audio_file_path = os.path.join(static_dir, filename)

    # Generate the audio speech
    response = openai_client.audio.speech.create(
        model="tts-1-hd",
        voice="onyx",
        input=input_text
    )

    # Save the audio file to the specified path
    response.stream_to_file(audio_file_path)

    return audio_file_path

def transcribe_voice_to_text(audio_file_path):
    initialize_openai_client()
    if not openai_client:
        raise Exception("OpenAI client is not initialized. Please set the OpenAI API key in User Preferences.")
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcript = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        print("API Response:", transcript)  # Print the response to verify

        return transcript  # Directly return the transcript
    except Exception as e:
        raise e

