#app.py
import json
from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import tempfile
from werkzeug.utils import secure_filename
import openai
from dotenv import load_dotenv
from OpenAIModels.textgen import generate_text

app = Flask(__name__)

# Load environment variables
load_dotenv('credentials.env')
api_key = os.getenv('OPENAI_API_KEY')
# client = openai.OpenAI(api_key=api_key)
openai.api_key = api_key

# Load or initialize conversation thread
def load_conversation_thread():
    try:
        with open('storage/conversation.json', 'r') as file:
            content = file.read()
            if not content:  # Check if the file is empty
                # Initialize with the first question
                first_question = {
                    "SalesRep": "Hey, glad you're here with us. Can you start by telling us what you plan on building as a platform?"
                }
                return [first_question]  # Return a list containing the first question
            return json.loads(content)
    except FileNotFoundError:
        # If the file doesn't exist, also initialize with the first question
        first_question = {
            "SalesRep": "Hey, glad you're here with us. Can you start by telling us what you plan on building as a platform?"
        }
        return [first_question]

def save_conversation_thread(conversationthread):
    with open('storage/conversation.json', 'w') as file:
        json.dump(conversationthread, file)

# Function to transcribe voice to text using OpenAI's API
def transcribe_voice_to_text(audio_file_path):
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        print("API Response:", transcript)  # Print the response to verify
        return transcript  # Directly return the transcript
    except Exception as e:
        raise e

def ClientOnboarder(conversationthread):
    print("Thinking of next question to ask...")
    #List of questions the AI Chatbot needs to ask to the user one a time as it sees information is not collected yet in the conversation.
    ExampleQuestions = """THese questions are ment to inspire your thought process, these questions represents elements of information we have to collect from the USer. the intention is to collect the required infromation for the successfull planning of a custom software project. Each Question Below should be addressed directly or indirectlym so when thinking of the next question you should analyze the conversation and see what information is missing from the desired information collection we would get by asking the below questions. If the user doesnt know and says they don't know, you can provide suggestions and ask if the user is okay with the suggestion.
                    What are some of the issues you're facing or problems you would like solved using custom software or digital platform?
                    What is the purpose of the digital Platform you wish to build?
                    What are the stakeholders or platform users that will use the software?
                    Please provide more about {Stakeholder 1, 2, 3, .. N} roles and responsibilities in the context of the platform.
                    Please provide the features required for each stake holder. {Stakeholder 1, 2, 3, … N}
                    Tell me about the interface information for {Stakeholder 1, 2, 3, ... N}. Is it going to be a Mobile app, Mobile app and website, or Only a website? If Mobile app [for options 1, and 2]"
                    Should the platform work on larger devices like Tablets and iPads as well?
                    Should the App be built for Android, iOS OR both?
                    """

    system_context = f"You are a salesrep for Myte, an AI Automation Agency. You ask questions to get an idea of the software development project the user wishes to do.Inspire yourself from the following questions, but use your judgement to ask the most pertinent next question to the user: {ExampleQuestions}. "
    assistant_context = "You provide concise questions around the Business Analysis phase of a software development project to understand project requirements."
    initial_prompt = f"Based on the conversation thread {conversationthread} provide the next best question to ask the user depending on what has not been answered yet, it doesnt need to be exactly the list of questions in your training base. We should however touch on the information type required from the list of questions in yourdata set. Be Creative to get the information from the user.  Only provide the next best question to as question adapted to the conversation with the user. If after verifying the list of questions, you have collected all required information respond with; Alright, that's enough information, give use a few moments and we will draft a detailed execution plan for you! Thanks for your time."

    SalesRepQuestion = generate_text(system_context, assistant_context, initial_prompt)
    return SalesRepQuestion

# Convert text to speech
def text_to_speech(input_text):
    response = openai.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=input_text
    )
    audio_file_path = "static/response_audio.mp3"
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
        text = transcribe_voice_to_text(audio_file_path)  # Call your transcription function
        return jsonify({"text": text})
    finally:
        os.remove(audio_file_path)
        os.rmdir(temp_dir)

@app.route('/submit_response', methods=['POST'])
def submit_response():
    data = request.get_json()  # This parses the JSON body of the request
    user_response = data['response']
    conversationthread = load_conversation_thread()

    # Append user response to the conversation thread
    conversationthread.append({"UserResponse": user_response})

    # Generate the next question
    next_question = ClientOnboarder(conversationthread)

    # Append the next question by salesrep to conversation thread
    conversationthread.append({"SalesRep": next_question})

    # Save updated conversation thread
    save_conversation_thread(conversationthread)

    # Convert the next question to speech
    audio_file_path = text_to_speech(next_question)  # Ensure this saves the file to 'static/response_audio.mp3'

    # Return the next question and the path to the audio file (relative to the static directory)
    return jsonify({"nextQuestion": next_question, "audioFilePath": "/static/response_audio.mp3"})

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True, port=1005)