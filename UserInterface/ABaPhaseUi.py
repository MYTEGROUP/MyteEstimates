from OpenAIModels.OpenAIClient import generate_text, text_to_speech, transcribe_voice_to_text
from tools.JsonOperators import get_base_path_audio,get_base_path,load_json_data,save_json_data
import threading
import tkinter as tk
from PIL import Image, ImageTk
import os
from tkinter import messagebox
import json
import sys
import pygame
from scipy.io.wavfile import write
import sounddevice as sd
import numpy as np
from tools.AGetAPIKeyInstructions import display_instructions
import webbrowser
from json.decoder import JSONDecodeError
from dotenv import load_dotenv

welcome_message = "Hey, glad you're here with us! Can you start by telling us what you plan to build as a platform?"
# Set the final message of the conversation
final_message = ("Great! Enjoy the future of outreach! We are crafting a personalized system based on our conversation, please hold on and a new window will appear.")

def initialize_conversation_file():
    # Define initial conversation data
    initial_data = {
        "conversation": [
            {
                "role": "Business Analyst",
                "message": f"{welcome_message}"
            }
        ]
    }

    # Ensure the Storage directory exists
    storage_dir = os.path.join(get_base_path(), 'storage')
    if not os.path.exists(storage_dir):
        os.makedirs(storage_dir)

    # Path to the OnboardConversation.json file
    file_path = os.path.join(storage_dir, 'BaPhase.json')

    # Write (or overwrite) the file with the initial data
    with open(file_path, 'w', encoding='utf-8') as f:  # 'w' mode will create or overwrite the file
        json.dump(initial_data, f, indent=4, ensure_ascii=False)


def record_voice():
    global recording_thread
    recording_thread = threading.Thread(target=start_recording)
    recording_thread.start()


def start_recording():
    global recording, rec_frames
    recording = True
    rec_frames = []
    frame_count = 0  # Initialize a frame counter
    sample_rate = 44100  # Audio sample rate
    segment_length = 3  # Segment length in seconds
    frames_per_buffer = 1024  # Number of frames per buffer, adjust as needed
    frames_per_segment = segment_length * sample_rate  # Calculate the number of frames in each 10-second segment

    def transcribe_segment(segment_data):

        # Ensure the temp directory exists
        temp_dir = os.path.join(get_base_path(), 'temp')
        os.makedirs(temp_dir, exist_ok=True)

        # Save the current segment to a temporary file
        segment_path = os.path.join(get_base_path(), 'temp', 'segment.wav')
        write(segment_path, sample_rate, segment_data)

        # Transcribe the segment
        try:
            transcribed_text = transcribe_voice_to_text(segment_path)
            # Extract the current text content from the user response area
            current_text = user_response_area.get("1.0", tk.END).strip()
            # Form the new text by appending the transcribed text to the current content
            # Add a space before the transcribed text if the current content is not empty
            new_text = current_text + (" " if current_text else "") + transcribed_text
            # Clear the current text and replace it with the new text
            window.after(0, lambda: user_response_area.delete("1.0", tk.END))
            window.after(0, lambda: user_response_area.insert("1.0", new_text))
        except Exception as e:
            print(f"Error transcribing segment: {e}")

    def transcribe_segment_in_thread(segment_data):
        # Start a new thread for transcribing the segment
        threading.Thread(target=transcribe_segment, args=(segment_data,), daemon=True).start()

    def callback(indata, buffer_frames, time, status):
        nonlocal frame_count
        rec_frames.append(indata.copy())
        frame_count += buffer_frames  # Using buffer_frames instead of frames

        # Update volume level in the UI
        window.after(0, lambda: volume_label.config(text=f"Volume: {int(np.linalg.norm(indata) * 10)}"))

        # Once we have enough frames for a 10-second segment, transcribe it in a separate thread
        if frame_count >= frames_per_segment:
            segment_data = np.concatenate(rec_frames[-int(frames_per_segment / buffer_frames):])
            # Schedule the transcription in a separate thread without directly updating the GUI
            threading.Thread(target=transcribe_segment_in_thread, args=(segment_data,), daemon=True).start()
            frame_count = 0

    with sd.InputStream(samplerate=sample_rate, blocksize=frames_per_buffer, callback=callback):
        while recording:
            window.update()
            sd.sleep(100)
    # Transcribe any remaining audio not part of a complethttps://www.linkedin.com/in/nicola-maggio-073a7263/
    # e 10-second segment
    if frame_count > 0:
        segment_data = np.concatenate(rec_frames[-int(frame_count / frames_per_buffer):])
        transcribe_segment_in_thread(segment_data)


def stop_recording():
    global recording
    recording = False
    recording_thread.join()

    # Optionally, after a delay, clear the status message
    window.after(3000, lambda: status_label.config(text=""))


def threaded_stop_recording():
    stop_thread = threading.Thread(target=stop_recording, daemon=True)
    stop_thread.start()


def threaded_submit_response():
    submit_thread = threading.Thread(target=submit_response, daemon=True)
    submit_thread.start()


def submit_response():
    user_response = user_response_area.get("1.0", tk.END).strip()
    if user_response:
        # Immediately display "Thinking of the next question" message
        status_label.config(text="Thinking of the next question...")

        # Append user response to the conversation
        append_to_conversation_file("UserResponse", user_response)

        # Clear the user response area
        user_response_area.delete("1.0", tk.END)

        # Generate the next question using the updated conversation
        next_question = ClientOnboarder()

        # Append the next question to the conversation
        append_to_conversation_file("Business Analyst", next_question)

        # Update the question area with the next question
        question_area.delete("1.0", tk.END)
        question_area.insert(tk.END, f"\nMyteOnboarder: {next_question}\n")

        # Ensure the UI updates to show the new question before playing audio
        window.update_idletasks()  # or window.update()

        # Generate the audio file for the next question and get its file path
        audio_file_path = text_to_speech(next_question)

        # Play the audio file containing the next question
        play_audio(audio_file_path)

        # Remove the "Thinking of the next question" message after playing the audio
        status_label.config(text="")

        # Check if the onboarding process is complete
        if next_question == final_message:
            # Show the temporary popup with the message
            show_temporary_popup("Creating your personalized Myte Social System...")
    else:
        user_response_area.insert(tk.END, "\n[No input detected. Please type or record your response.]\n")


def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Wait for the music to play before moving on
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Stop and unload the music to release the file
    pygame.mixer.music.stop()
    if hasattr(pygame.mixer.music, 'unload'):  # Check if 'unload' is available
        pygame.mixer.music.unload()  # Unload the music file to free up resources


def append_to_conversation_file(role, message):
    file_path = os.path.join(get_base_path(), 'storage', 'OnboardConversation.json')
    # Ensure the file exists with a default structure
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:  # Specify UTF-8 encoding
            json.dump({"conversation": []}, f, indent=4)

    # Open the file and read the data
    with open(file_path, 'r+', encoding='utf-8') as f:  # Specify UTF-8 encoding
        data = json.load(f)
        if 'conversation' not in data:
            data['conversation'] = []
        data['conversation'].append({'role': role, 'message': message})
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


def ClientOnboarder():
    file_path = os.path.join(get_base_path(), 'storage', 'OnboardConversation.json')
    # Check if file exists, if not, create it with an initial structure
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump({"conversation": []}, f, indent=4)

    with open(file_path, 'r') as f:
        conversationthread = json.load(f)

    # Convert the conversation thread into a format suitable for the AI model
    conversation_string = "\n".join([f"{k}: {v}" for k, v in conversationthread.items()])

    print("Thinking of next question to ask...")
    # List of questions the AI Chatbot needs to ask to the user one a time as it sees information is not collected yet in the conversation.
    ExampleQuestions = """
                           What are some of the issues you're facing or problems you would like solved using custom software or digital platform?
                           What is the purpose of the digital Platform you wish to build?
                           What are the stakeholders or platform users that will use the software?
                           Please provide more about {Stakeholder 1, 2, 3, .. N} roles and responsibilities in the context of the platform.
                           Please provide the features required for each stakeholder. {Stakeholder 1, 2, 3, … N}
                           Tell me about the interface information for {Stakeholder 1, 2, 3, ... N}. Is it going to be a Mobile app, Mobile app and website, or Only a website? If Mobile app [for options 1, and 2]"
                           Should the platform work on larger devices like Tablets and iPads as well?
                           Should the App be built for Android, iOS OR both?
                           """

    system_context = (
        f"You are a Business Analyst for Myte Group Inc. an AI Automation Agency. Your Name is Myte. You ask questions to get an idea of the project requirements of the client."
        f"Inspire yourself from the following questions, but use your judgement to ask the most pertinent and personalized next question to the user: {ExampleQuestions}."
        f"The provided questions are meant to inspire your thought process of determining the next best question to collect missing information we need for a good enough high-level estimate."
        f"The intention is to collect required information for the successful research & planning of a custom software projec in a later phase. We want to capture Functional Requirements"
        f"When thinking of the next question you should analyze the conversation and see what information is missing."
        f"When asking the question also provide personalized examples the user can be inspired of to provide their answer."
        )
    assistant_context = "You provide questions around the Business Analysis phase of a software development project to understand project requirements, your questions should be in a converational manner, simple and light language, so the general public can understand."
    initial_prompt = (
        f"Based on the conversation thread {conversation_string} provide the next best question to ask the user depending on critical information needed for the successfull planning of functionalities (backend/Frontend logic) to make their vision a reality."
        f"Use the example questions as inspiration."
        f"If after verifying the list of questions, you have collected all required information or you identified that more than 15 questions have already been asked, respond with; {final_message}")


    next_question = generate_text(system_context, assistant_context, initial_prompt)

    # Checker of response for final message QUality Check.
    system_context_checker = (
        f"You quality control a response. You're checking for the presence of the final message: '{final_message}'."
        f" If it's present or ressembles it, respond 'Yes', otherwise respond 'No'. Respond only 'Yes' or 'No'."
    )
    assistant_context_checker = "Respond with 'Yes' or 'No' only."
    initial_prompt_checker = (f"Read the response: {next_question}. Is the final message present in the response?")

    response_checker = generate_text(system_context_checker, assistant_context_checker, initial_prompt_checker)

    if response_checker.lower() == 'yes':
        return final_message
    else:
        return next_question




def check_onboarding_status():
    status_file_path = os.path.join(get_base_path(), 'storage', 'User_Onboarding_Status.json')
    # Check if file exists, if not, create it with an initial structure
    if not os.path.exists(status_file_path):
        with open(status_file_path, 'w') as f:
            json.dump({"MyteOnboardStatus": False, "initial_setup_completed": False}, f, indent=4)
        return False  # Assuming default onboarding status is False

    with open(status_file_path, 'r') as f:
        status_data = json.load(f)
    return status_data.get("MyteOnboardStatus", False)


def update_next_step_button_color(button, status):
    if status:
        button.config(bg='green', fg='white')
    else:
        button.config(bg='red', fg='white')


# Validation to close The_Onboarder UI and proceed to the next UI.ag
def proceed_to_next_step():
    # Close any open popups first
    close_temporary_popup()

    # Check if the onboarding window still exists
    if window.winfo_exists():
        # Cancel scheduled tasks to clean up any remaining references
        window.after_cancel(check_onboarding_status_id)
        window.after_cancel(schedule_api_key_check_id)

        # Close the onboarding window properly
        window.destroy()

    # Initialize the next part of the UI in a fresh root context
    root = tk.Tk()
    #SET UP NEXT STEP AFTER CONVERATION DONE.
    root.mainloop()


def check_onboarding_status_and_update_button():
    if window.winfo_exists():  # Check if window still exists
        onboarding_complete = check_onboarding_status()
        update_next_step_button_color(next_step_button, onboarding_complete)


def update_next_step_button_color(button, status):
    if status:
        button.config(bg='green', fg='white')
    else:
        button.config(bg='red', fg='white')


def check_api_key_and_update_button():
    try:
        load_dotenv(os.path.join(get_base_path(), '.env'))
        api_key = os.getenv('OPENAI_API_KEY', '')
        if api_key:  # If the API key exists and is not empty
            get_api_key_button.config(bg='green', fg='white')
        else:
            get_api_key_button.config(bg='red', fg='white')
    except Exception:
        get_api_key_button.config(bg='red', fg='white')


# Schedule the function to check the API key periodically
def schedule_api_key_check():
    if window.winfo_exists():  # Check if window still exists
        check_api_key_and_update_button()


def center_window(window):
    """
    Center a Tkinter window on the user's screen.
    Call this after defining the window size.
    """
    window.update_idletasks()  # Update the internal state of the window
    width = window.winfo_width()  # Get the width of the window
    height = window.winfo_height()  # Get the height of the window
    screen_width = window.winfo_screenwidth()  # Get the width of the screen
    screen_height = window.winfo_screenheight()  # Get the height of the screen

    # Calculate x and y coordinates based on screen and window dimensions
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)

    # Set the window's position
    window.geometry(f'{width}x{height}+{x}+{y}')


def check_api_key_before_action(action):
    try:
        load_dotenv(os.path.join(get_base_path(), '.env'))
        api_key = os.getenv('OPENAI_API_KEY', '')
        if not api_key:
            messagebox.showerror("API Key Required", "Please get your API Key first.")
            return
        else:
            action()
    except Exception:
        messagebox.showerror("API Key Required", "Please get your API Key first.")


def record_voice_checked():
    check_api_key_before_action(record_voice)


def open_browser_and_display_instructions():
    # Open the desired URL in the default web browser
    webbrowser.open_new("https://openai.com/api")
    # Display the instructions in a new window
    display_instructions(window)


def show_temporary_popup(message):
    global temp_popup
    temp_popup = tk.Toplevel(window)  # Create a new top-level window
    temp_popup.title("Please Wait...")

    # Configure the temporary popup dimensions
    temp_popup.geometry('400x150')  # Example dimensions; adjust as needed

    message_label = tk.Label(temp_popup, text=message, font=("Comic Sans MS", 12))
    message_label.pack(pady=20, padx=20)  # Adjust padding as needed

    center_window(temp_popup)  # Center the popup after setting the size

    # Disable interaction with the main window while the popup is open
    temp_popup.grab_set()


def close_temporary_popup():
    if 'temp_popup' in globals() and temp_popup.winfo_exists():
        temp_popup.grab_release()  # Allow interaction with the main window
        temp_popup.destroy()


def The_Onboarder():
    global window, user_response_area, question_area, volume_label, status_label, next_step_button, get_api_key_button
    initialize_conversation_file()

    # Preload the welcome audio
    pygame.mixer.init()
    welcome_audio_path = os.path.join(get_base_path_audio(), 'static', 'InitialGreeting.mp3')
    pygame.mixer.music.load(welcome_audio_path)

    # Initialize the Tkinter window
    window = tk.Tk()
    window.title("Business Analysis Phase")
    window.geometry("390x844")  # Adjusted for longer window
    center_window(window)  # Center window on screen
    window.grid_columnconfigure(0, weight=1)  # This will center all the widgets

    # Configure the buttons
    button_font = ("Comic Sans MS", 10)
    button_pady = 10
    button_sticky = "ew"

    # Schedule the tasks and keep their IDs
    global check_onboarding_status_id, schedule_api_key_check_id
    check_onboarding_status_id = window.after(500, check_onboarding_status_and_update_button)
    schedule_api_key_check_id = window.after(5000, schedule_api_key_check)

    logo_path = os.path.join(get_base_path_audio(), 'static', 'Logo.png')
    original_logo_image = Image.open(logo_path)
    resized_logo_image = original_logo_image.resize((150, 75), Image.Resampling.LANCZOS)
    logo_image = ImageTk.PhotoImage(resized_logo_image)

    # Logo label
    logo_label = tk.Label(window, image=logo_image)
    logo_label.image = logo_image
    logo_label.grid(row=0, column=0, pady=(10, 0))

    # Add the title
    title_label = tk.Label(window, text="Myte Social - Social Media AI System", font=("Comic Sans MS", 12))
    title_label.grid(row=1, column=0, pady=(0, 10))

    # Question area
    question_area = tk.Text(window, height=5, width=50, bg='light grey', font=("Comic Sans MS", 10), wrap=tk.WORD)
    question_area.grid(row=2, column=0, padx=10, pady=(0, 10))

    # User response area
    user_response_area = tk.Text(window, height=10, width=50, font=("Comic Sans MS", 10), wrap=tk.WORD)
    user_response_area.grid(row=3, column=0, padx=10, pady=(0, 10))
    # Record button with API key check
    record_button = tk.Button(window, text="Record", font=button_font, command=record_voice_checked)
    record_button.grid(row=4, column=0, sticky=button_sticky, padx=10, pady=button_pady)

    stop_button = tk.Button(window, text="Stop Recording", font=button_font, command=threaded_stop_recording)
    stop_button.grid(row=5, column=0, sticky=button_sticky, padx=10, pady=button_pady)

    submit_button = tk.Button(window, text="Submit Response", font=button_font, command=threaded_submit_response)
    submit_button.grid(row=6, column=0, sticky=button_sticky, padx=10, pady=button_pady)

    volume_label = tk.Label(window, text="Volume: 0", font=button_font)
    volume_label.grid(row=7, column=0, pady=(10, 20))

    # "Get API Key" button
    get_api_key_button = tk.Button(window, text="Get API Key", bg='red', fg='white', font=button_font,
                                   command=open_browser_and_display_instructions)
    get_api_key_button.grid(row=8, column=0, sticky="ew", padx=10, pady=10)

    # "Next Step" button
    next_step_button = tk.Button(window, text="Next Step", font=button_font, command=proceed_to_next_step)
    next_step_button.grid(row=9, column=0, sticky="ew", padx=10, pady=10, columnspan=1)

    # Call the function to initially set the button color
    check_api_key_and_update_button()
    schedule_api_key_check()
    window.bind("<FocusIn>", lambda event: check_api_key_and_update_button())

    # Initialize the color of the Next Step button based on the current onboarding status
    check_onboarding_status_and_update_button()

    # Initialize the conversation file and display the welcome message
    question_area.insert(tk.END, f"MyteOnboarder: {welcome_message}\n")

    # Status label for displaying messages
    status_label = tk.Label(window, text="", fg="green", font=("Comic Sans MS", 10))
    status_label.grid(row=10, column=0, pady=(10, 10))  # Add appropriate row and column indices

    # Play the welcome audio
    pygame.mixer.music.play()

    window.mainloop()


if __name__ == "__main__":
    The_Onboarder()




