import json
import time
from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import tempfile
from werkzeug.utils import secure_filename
import openai
from dotenv import load_dotenv
from OpenAIModels.textgen import generate_text  # Assuming this is defined in textgen.py and works as expected

app = Flask(__name__)

# Load environment variables
load_dotenv('credentials.env')
api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = api_key

# Load or initialize conversation thread
def load_conversation_thread():
    try:
        with open('storage/conversation.json', 'r') as file:
            content = file.read()
            if not content:  # Check if the file is empty
                first_question = {
                    "SalesRep": "Hey, glad you're here with us. Can you start by telling us what you plan on building as a platform?"
                }
                return [first_question]  # Return a list containing the first question
            return json.loads(content)
    except FileNotFoundError:
        first_question = {
            "SalesRep": "Hey, glad you're here with us. Can you start by telling us what you plan on building as a platform?"
        }
        return [first_question]

def save_conversation_thread(conversationthread):
    with open('storage/conversation.json', 'w') as file:
        json.dump(conversationthread, file)

def transcribe_voice_to_text(audio_file_path):
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcript = openai.Audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        return transcript
    except Exception as e:
        raise e

def ClientOnboarder(conversationthread):
    print("Thinking of next question to ask...")
    ExampleQuestions = """
                       These questions are meant to inspire your thought process, these questions represent elements of information we have to collect from the User. The intention is to collect the required information for the successful planning of a custom software project. Each Question Below should be addressed directly or indirectly, so when thinking of the next question you should analyze the conversation and see what information is missing from the desired information collection we would get by asking the below questions. If the user doesn't know and says they don't know, you can provide suggestions and ask if the user is okay with the suggestion.
                       What are some of the issues you're facing or problems you would like solved using custom software or digital platform?
                       What is the purpose of the digital Platform you wish to build?
                       What are the stakeholders or platform users that will use the software?
                       Please provide more about {Stakeholder 1, 2, 3, .. N} roles and responsibilities in the context of the platform.
                       Please provide the features required for each stakeholder. {Stakeholder 1, 2, 3, … N}
                       Tell me about the interface information for {Stakeholder 1, 2, 3, ... N}. Is it going to be a Mobile app, Mobile app and website, or Only a website? If Mobile app [for options 1, and 2]"
                       Should the platform work on larger devices like Tablets and iPads as well?
                       Should the App be built for Android, iOS OR both?
                       """

    system_context = (f"You are a sales rep for Myte, an AI Automation Agency. You ask questions to get an idea of the software development project the user wishes to do."
                      f"Inspire yourself from the following questions, but use your judgement to ask the most pertinent next question to the user: {ExampleQuestions}. "
                      )
    assistant_context = "You provide concise questions around the Business Analysis phase of a software development project to understand project requirements."
    initial_prompt = f"Based on the conversation thread {conversationthread} provide the next best question to ask the user depending on what has not been answered yet, it doesn't need to be exactly the list of questions in your training base. We should however touch on the information type required from the list of questions in your data set. Be Creative to get the information from the user. Only provide the next best question to ask adapted to the conversation with the user. If after verifying the list of questions, you have collected all required information respond with; Alright, that's enough information, give us a few moments and we will draft a detailed execution plan for you! Thanks for your time."

    SalesRepQuestion = generate_text(system_context, assistant_context, initial_prompt)
    return SalesRepQuestion

def text_to_speech(input_text):
    response = openai.Audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=input_text
    )
    timestamp = int(time.time())
    temp_dir = tempfile.mkdtemp()
    audio_file_path = os.path.join(temp_dir, f"response_audio_{timestamp}.mp3")
    response.stream_to_file(audio_file_path)
    return audio_file_path

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    temp_dir = tempfile.mkdtemp()
    audio_file_path = os.path.join(temp_dir, secure_filename(audio_file.filename))
    audio_file.save(audio_file_path)

    try:
        text = transcribe_voice_to_text(audio_file_path)
        return jsonify({"text": text})
    finally:
        os.remove(audio_file_path)
        os.rmdir(temp_dir)

@app.route('/submit_response', methods=['POST'])
def submit_response():
    data = request.get_json()
    user_response = data['response']
    conversationthread = load_conversation_thread()

    conversationthread.append({"UserResponse": user_response})

    next_question = ClientOnboarder(conversationthread)
    conversationthread.append({"SalesRep": next_question})

    save_conversation_thread(conversationthread)

    audio_file_path = text_to_speech(next_question)
    temp_dir, audio_filename = os.path.split(audio_file_path)

    return jsonify({"nextQuestion": next_question, "audioDir": temp_dir, "audioFile": audio_filename})

@app.route('/serve_audio/<path:directory>/<filename>')
def serve_audio(directory, filename):
    return send_from_directory(directory, filename)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True, port=1010)
