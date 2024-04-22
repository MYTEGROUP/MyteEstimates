#1Vision2Stories.py
import json
from OpenAIModels.textgen import generate_text, generate_text_json
import threading
from collections import OrderedDict
import tkinter as tk
from tkinter import scrolledtext
import queue
import time


# Functions to process a single section of Project Requirement Template and update its response
def process_section(index, description_data, initial_description, updated_data):
    section = description_data["Section"]
    description = description_data["Description"]

    question = f"{section}: {description}"

    print(f"Processing: {question}")
    response = process_question(initial_description, question)

    # Include the index in the data structure to maintain order
    updated_data.append({
        "index": index,
        "data": {
            "Section": section,
            "Description": description,
            "Response": response
        }
    })
def process_question(initial_requirements, description):
    # Assuming the 'description' serves as the question
    system_context = "You're a Product Architect and your task is to answer the Project Requirement section provided based solely on the initial project requirements received. Your response is assertive and logical and written in high-school level simple language."
    assistant_context = ""
    initial_prompt = f"Given the initial project requirements: {initial_requirements}, explain the following section of our Project Requirement file in detail using only the provided initial requirements: {description}. Only use the provided initial description. If there is lacking information, say so and provide a logical answer solely based on the provided intial description."

    response = generate_text(system_context, assistant_context, initial_prompt)
    return response

#Establish Vision, Business Verticles, Primary Stakeholders, Revenue Models for each Stake Holder

def Project_Vision(Project_Requirements):
    print("Creating Project Vision...")
    system_context = ("Your a Product Architect and your task is to provide a concise project vision based on the requirements you receive.")
    assistant_context = ""
    initial_prompt = (f"Here is the project requirements for context: {Project_Requirements}."
                      f"Write a 200 words project vision, it should be exciting and attention grabbing")

    projectvision = generate_text(system_context, assistant_context, initial_prompt)
    return projectvision


def Business_Verticles(Project_Requirements):
    print("Creating Business Verticals...")
    system_context = (
        "As a Product Architect, your task is to identify potential business or industry sector that the project might cater to or impact. "
        "Business verticals refer to distinct categories within the business world that the project might apply to, such as finance, healthcare, "
        "education, etc. "
        "Keep the vertical name concise, ideally not more than three words and provide the BEST verticle - your response should be 1 Business Vertical"
        "that best suits the Project Requirements you are given."
    )
    assistant_context = ("You need to respond in JSON format. The expected format is {'Business_Vertical': ['Vertical1']}."
                         "The vertical should be a concise name, no more than three words.")
    initial_prompt = (
        f"Based on the following project requirements: '{Project_Requirements}', identify the relevant business or industry sector (vertical) "
        f"the project could impact or be applied to the best. "
        "The verticle name being no more than three words. "
        "Respond in JSON format, using the key 'Business_Vertical'. your response should be 1 Business Vertical that best suits the Project Requirements you are given."
    )

    Business_Verticles_Response = generate_text_json(system_context, assistant_context, initial_prompt)
    return Business_Verticles_Response



def StakeHolders(Project_Requirements):
    print("Identifying End User Stakeholders...")
    system_context = (
        "As a Product Architect, you are tasked with identifying the primary users of the system based on the provided client requirements. "
        "These users should represent the comprehensive functionalities of the system, focusing on all specific actions and needs relative to the system. "
        "Consider that these user types might perform various tasks typically associated with multiple roles. "
        "Streamline the list the the core primary users."
    )

    assistant_context = "You need to respond in JSON format. The expected format is {'Stakeholders': ['User Role 1', 'User Role 2', 'User Role 3']}. Each role should be described concisely, using no more than five words."
    initial_prompt = (
        f"Based solely on the detailed project requirements provided in the description: '{Project_Requirements}', identify the primary users of the system. "
        "Describe the users interaction with the system comprehensively, covering all tasks they perform. Provide your response in JSON format, using the key 'Stakeholders'."
    )

    primary_stakeholders_response = generate_text_json(system_context, assistant_context, initial_prompt)
    return primary_stakeholders_response



def Revenue_Model(Project_Requirements, primary_stakeholders):
    print("Determining Revenue Models...")
    system_context = (
        "As a Product Architect, your task is to identify the most suitable revenue model for each primary stakeholder of the product, "
        "considering the product description and stakeholder roles. "
        "For stakeholders with a clear path to revenue generation, select from 'direct payment', 'subscription', or 'commission'. "
        "Provide a rationale for each suggested model, including who pays, what they pay for, and who receives the revenue."
    )
    assistant_context = (
        "You need to respond in JSON format. The expected format is "
        "{'RevenueModels': [{'Stakeholder': 'User Role 1', 'Model': 'Subscription', 'Rationale': 'Explanation 1'}, {...}]} "
        "where each object in the 'RevenueModels' array contains the stakeholder role, selected revenue model, and a brief explanation."
    )
    initial_prompt = (
        f"Given the client requirements: '{Project_Requirements}' and the identified primary stakeholders: {primary_stakeholders}, "
        "suggest the most appropriate revenue model for each stakeholder. Include a brief explanation for each choice, "
        "addressing who pays, what the payment is for, and who receives the revenue. "
        "Format your response in JSON, using the key 'RevenueModels' and providing a list where each item is an object containing 'Stakeholder', 'Model', and 'Rationale'."
    )

    revenue_model_response = generate_text_json(system_context, assistant_context, initial_prompt)
    return revenue_model_response

#Functions to Process Project Requirements and Initial Client Requirements, and establish Epics for each stakeholder
def Define_Epics(Project_Requirements, Stakeholder, Initial_Requirements):
    print("Defining Epics for Agile Scrum Development...")
    print(f"{Project_Requirements}")

    system_context = (
        "As a Product Architect, analyze the provided project requirements "
        "to define high-level Epics for Agile Scrum development tailored to the specific needs of the stakeholder relative to the project requirements."
        "List Epics based on all the functionalities found only in the Project Requirements provided."
    )
    assistant_context = (
        "You need to respond in JSON format. The expected format is "
        "{'Stakeholder': '{Stakeholder}', 'Epics': [{'Title': 'Epic Title 1', 'Description': 'Description of what the epic will achieve'}, {...}]} "
        "where each object in the 'Epics' array contains a 'Title' and 'Description' for each epic tailored to the needs of the stakeholder."
    )
    initial_prompt = (
        f"Based solely on the initial client requirements : [{Initial_Requirements}] and the detailed project requirements : [{Project_Requirements}] provide a list of Epics focusing on the needs of this stakeholder '{Stakeholder}', "
        "Format your response as a JSON object with the stakeholder name as a key and an array of epics, "
        "each epic represented by a 'Title' and 'Description'. Do not include IDs in the initial generation."
    )

    epics_response = generate_text_json(system_context, assistant_context, initial_prompt)
    print(f"Here is the epics_response: {epics_response}")
    try:
        # Assuming epics_response is already a JSON string, parse it to a Python dict.
        epics_data = json.loads(epics_response)
        formatted_epics = {
            Stakeholder: epics_data['Epics']
        }
        return formatted_epics
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response for {Stakeholder}. Error: {e}")
        return {}

def thread_function(Project_Requirements, stakeholder, stakeholder_epics, Initial_Requirements):
    epics = Define_Epics(Project_Requirements, stakeholder, Initial_Requirements)
    formatted_epics = []
    if isinstance(epics, dict) and stakeholder in epics:
        for i, epic in enumerate(epics[stakeholder]):
            epic_id = f"E{str(i+1).zfill(3)}"  # Format as E001, E002, etc.
            formatted_epics.append({
                "Epic ID": epic_id,
                "Title": epic['Title'],
                "Description": epic['Description']
            })
    with threading.Lock():
        stakeholder_epics[stakeholder] = formatted_epics

def process_all_stakeholders(Project_Requirements, stakeholders,Initial_Requirements):
    stakeholder_epics = {}
    threads = []
    for stakeholder in stakeholders:
        thread = threading.Thread(target=thread_function, args=(Project_Requirements, stakeholder, stakeholder_epics, Initial_Requirements))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return stakeholder_epics


#Function to establish User Stories for Each Epics and Stakeholder
def define_user_stories(epic, stakeholder, list_of_epics, list_of_stakeholders, project_requirements, client_requirements):
    system_context = (
        "As a Product Architect involved in Agile Scrum development, your provided with stake holder, epics, requirements and the initial client requirements."
        "Based solely on the provided information, your task is to take a high-level Epic provided within its project context "
        "and break it down into detailed, actionable user stories. Each user story should represent a specific functionality or feature to be developed, "
        "focusing on delivering value to the primary stakeholder identified in the project. The stories should be concise, testable, and provide clear acceptance criteria."
        "If Critical logical elements are missing from the requirements context, such as Login/Access to the platform for the stakholder, Password Recovery/reset please include it as those are often skipped when"
        "capturing initial requirements from the client."
    )
    assistant_context = (
        "Respond with a JSON object where each 'UserStories' array contains objects with the keys 'Title', 'Description', and 'AcceptanceCriteria'. "
        "Ensure the stories are granular enough to be completed within a single sprint and contribute directly to achieving the goals of the Epic and Stakeholder"
        "Make sure to use 'UserStories' as the key for the array of stories and 'Acceptance Criteria' as the key for the list of criteria within each story. "
        "Each 'Description' should follow the Agile Scrum user story format: 'As a [role], I want [feature] so that [benefit]'."
    )
    initial_prompt = (
        f"Given the Epic: {epic} and the stakeholder: {stakeholder}, along with the following context: project requirements: {project_requirements}, "
        f"initial client requirements:{client_requirements}, the primary stakeholders: {list_of_stakeholders}, and the global list of epics: {list_of_epics}, "
        "define a list of user stories for this stakeholder and epic. "
        "These stories should detail the specific functionalities or features needed to fulfill the objectives of the Epic, tailored to the needs of the stakeholder. "
        "Respond with a JSON object structured with keys for 'Title', 'Description', and 'AcceptanceCriteria'. "
        "Each 'Description' should follow the Agile Scrum user story format: 'As a [role], I want [feature] so that [benefit]'."

    )

    stories = generate_text_json(system_context, assistant_context, initial_prompt)
    return json.loads(stories)

def process_stakeholder_epic(epic_index, epic, stakeholder, project_requirements, client_requirements, results, lock, story_counters):
    list_of_epics = json.dumps([epic])  # Serialize for context
    list_of_stakeholders = json.dumps([stakeholder])  # Simplifying the context
    user_stories = define_user_stories(epic['Description'], stakeholder, list_of_epics, list_of_stakeholders, project_requirements, client_requirements)
    formatted_stories = []

    with lock:  # Using the lock to safely handle story ID counters and result appending
        if stakeholder not in story_counters:
            story_counters[stakeholder] = 1  # Initialize story counter for the stakeholder if not already done

        story_count = story_counters[stakeholder]
        for story in user_stories['UserStories']:
            story_id = f"S{story_count:03d}"
            story_count += 1
            formatted_stories.append({
                "Story ID": story_id,
                "Title": story['Title'],
                "Description": story['Description'],
                "AcceptanceCriteria": story['AcceptanceCriteria']
            })

        # Update the story counter for this stakeholder
        story_counters[stakeholder] = story_count

        # Append the epic and its stories in the correct order
        results[stakeholder][epic_index] = {
            "Epic ID": epic['Epic ID'],
            "Title": epic['Title'],
            "Description": epic['Description'],
            "User Stories": formatted_stories
        }

def process_epics():
    with open('storage/Epics.json', 'r') as file:
        epics_data = json.load(file)

    with open('storage/Project_Requirements.json', 'r') as file:
        project_requirements = json.load(file)

    with open('storage/Initial_Client_Requirements.json', 'r') as file:
        client_requirements = json.load(file)

    # This will store the final results with proper IDs
    final_results = {}

    threads = []
    lock = threading.Lock()

    # Processing each stakeholder independently
    for stakeholder, epics in epics_data['Stakeholder_Epics'].items():
        final_results[stakeholder] = []
        all_stories = []  # To hold stories with their epics

        for epic in epics:
            print(f"Processing epic {epic['Title']} for stakeholder {stakeholder}")
            thread = threading.Thread(target=collect_stories, args=(
            epic, stakeholder, project_requirements, client_requirements, all_stories, lock))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # After all stories are collected, sort them by Epic ID (if not already sorted), then assign story IDs
        all_stories.sort(key=lambda x: x['Epic ID'])
        story_id = 1
        for story_group in all_stories:
            for story in story_group['User Stories']:
                story['Story ID'] = f"S{story_id:03d}"
                story_id += 1

            # Append to final results
            final_results[stakeholder].append(story_group)

        # Save to JSON
    with open('storage/ProjectBreakdown.json', 'w') as file:
        json.dump(final_results, file, indent=4)

    print("Project breakdown with user stories for each stakeholder has been successfully compiled and saved.")


def collect_stories(epic, stakeholder, project_requirements, client_requirements, all_stories, lock):
    # Generate user stories for the given epic
    stories = define_user_stories(epic['Description'], stakeholder, [epic], [stakeholder], project_requirements, client_requirements)
    story_data = {
        "Epic ID": epic['Epic ID'],
        "Title": epic['Title'],
        "Description": epic['Description'],
        "User Stories": stories['UserStories']
    }
    with lock:
        all_stories.append(story_data)

#Base Transformer Model using generate_text function - it's output is a string of text.
def XXXX(Variable):
    print("Creating Business Verticals..")
    system_context = ("Your a Product Architect and your task is to ")
    assistant_context = ""
    initial_prompt = f"Here are the Client requirements: {Client_Requirements}."

    XXX = generate_text(system_context, assistant_context, initial_prompt)
    return XXX

def main():
    def get_description():
        # This function now merely closes the GUI
        root.quit()
    # Initialize the main GUI window
    root = tk.Tk()
    root.title("Project Description")

    # Add a label
    label = tk.Label(root, text="Please describe your vision here:")
    label.pack()

    # Create a scrolled text box
    text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
    text_box.pack()

    # Button to submit the description
    send_button = tk.Button(root, text="Send", command=get_description)
    send_button.pack()

    # Run the GUI
    root.mainloop()

    # Retrieve the text immediately after the main loop ends but before the root window is destroyed
    initial_description = text_box.get("1.0", "end-1c")
    # Prepare data to be saved in JSON format
    data = {
        "Initial Client Requirements": initial_description
    }

    # Save the data into a JSON file in the 'storage' directory
    with open('storage/Initial_Client_Requirements.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    root.destroy()  # Now destroy the root window safely after capturing the input

    with open('storage/project_description_template.json', 'r') as file:
        project_description_template = json.load(file)

    updated_project_description = []
    threads = []

    for index, description_data in enumerate(project_description_template):
        thread = threading.Thread(target=process_section, args=(index, description_data, initial_description, updated_project_description))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Sort the updated_project_description by index and extract the data
    ordered_project_description = [item["data"] for item in sorted(updated_project_description, key=lambda x: x["index"])]

    with open('storage/Project_Requirements.json', 'w') as file:
        json.dump(ordered_project_description, file, indent=4)

    print("Project requirements have been successfully processed and saved.")


    # Creating Summaries for Vision, Business Verticles, StakeHolders, Revenue Models
    with open('storage/Project_Requirements.json', 'r') as file:
        Project_Requirements = json.load(file)

    project_vision = Project_Vision(Project_Requirements)
    print(f"{project_vision}")

    business_verticles_json = Business_Verticles(Project_Requirements)
    print(f"{business_verticles_json}")

    stakeholders_json = StakeHolders(Project_Requirements)
    print(f"{stakeholders_json}")

    revenue_models_json = Revenue_Model(Project_Requirements, stakeholders_json)
    print(f"{revenue_models_json}")

    # Parse the JSON responses
    business_verticles = json.loads(business_verticles_json)
    stakeholders = json.loads(stakeholders_json)
    revenue_models = json.loads(revenue_models_json)

    # Compile all requirements into a simplified single structure
    project_requirements_short = {
        "Project Vision": project_vision,
        "Business Vertical": business_verticles['Business_Vertical'],
        "Stakeholders": stakeholders['Stakeholders'],
        "Revenue Models": revenue_models['RevenueModels']
    }

    # Save the compiled requirements to a JSON file
    with open('storage/ProjectSummary.json', 'w') as file:
        json.dump(project_requirements_short, file, indent=4)

    print("Short project requirements have been successfully compiled and saved.")

    #Creation of Epics
    # Load Project Requirements and Project Summary
    with open('storage/Project_Requirements.json', 'r') as file:
        Project_Requirements = json.load(file)

    with open('storage/ProjectSummary.json', 'r') as file:
        project_summary = json.load(file)

    with open('storage/Initial_Client_Requirements.json', 'r') as file:
        Initial_Requirements = json.load(file)

    stakeholders = project_summary['Stakeholders']

    # Generate and save epics for each stakeholder
    stakeholder_epics = process_all_stakeholders(Project_Requirements, stakeholders,Initial_Requirements)

    with open('storage/Epics.json', 'w') as file:
        json.dump({"Stakeholder_Epics": stakeholder_epics}, file, indent=4)

    print("Epics for each stakeholder have been successfully compiled and saved.")


   #Logic to create the Stories for each epic/Stakeholder

    process_epics()

    

if __name__ == "__main__":
    main()


