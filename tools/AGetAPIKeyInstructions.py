#AGetAPIKeyInstructions.py

import os
import sys
import tkinter as tk
import json
from json import JSONDecodeError
from tkinter import messagebox


def get_base_path():
    """Determine and return the base path for application data."""
    if getattr(sys, 'frozen', False):
        # If running in a PyInstaller bundle
        return os.path.dirname(sys.executable)
    else:
        # If running in a normal Python environment, move up one level
        return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))



def display_instructions(root):
    instructions = [
        "Log in or signup to ChatGPT by clicking 'Log in', top left of the screen.",
        "Once you are logged in - Two options appear: ChatGPT and API, click on 'API'.",
        "On the left menu bar, you will see 'Settings' - click on it.",
        "Then click on 'Billing'.",
        "Then click on 'Payment Methods' and add your payment method - once done click on 'Overview' to go back to the Billing settings.",
        "Now you can either 1: Add credit to balance or 2: Enable auto recharge. Each message costs about $0.1 to send. We are working on driving this cost down without impacting the quality of the AI system output in future updates.",
        "Now, On the left menu bar, click API KEYS",
        "Click on Create new secret key, then name it what you want with All permissions and click create secret key",
        "Copy the series of characters then click on,  the API key will be saved for your use on the system."
    ]

    def save_api_key():
        """Save the API key into the .env file."""
        clipboard_content = root.clipboard_get()  # Use the passed-in root Tk instance

        env_path = os.path.join(get_base_path(), '.env')

        lines = []
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()

        updated = False
        for i, line in enumerate(lines):
            if line.strip().startswith('OPENAI_API_KEY='):
                lines[i] = f'OPENAI_API_KEY={clipboard_content}'
                updated = True
                break
        if not updated:
            lines.append(f'OPENAI_API_KEY={clipboard_content}')

        try:
            with open(env_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(lines) + "\n")
            messagebox.showinfo("Success", "API key saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save API key: {e}")


    instruction_index = 0

    instruction_window = tk.Toplevel()
    instruction_window.title("Instructions")
    instruction_window.geometry("400x200+0+0")  # Size and position top-left
    instruction_window.attributes("-topmost", True)  # Always on top

    instruction_label = tk.Label(instruction_window, text=instructions[instruction_index], wraplength=380)
    instruction_label.pack(pady=20)

    def next_instruction():
        nonlocal instruction_index
        instruction_index += 1
        if instruction_index < len(instructions):
            instruction_label.config(text=instructions[instruction_index])
        else:
            save_api_key()
            instruction_window.destroy()


    next_button = tk.Button(instruction_window, text="Next", command=next_instruction)
    next_button.pack()

