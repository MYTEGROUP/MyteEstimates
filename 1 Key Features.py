#1 Key Features.py
import os
import json
from OpenAIModels.textgen import generate_text
from OpenAIModels.ListGenerator import generate_list
import itertools


# Global counter for FeatureListID and ProposalID
COUNTER_STATE_FILE = 'storage/counter_state.json'
feature_list_id_counter = itertools.count(start=1)
proposal_id_counter = itertools.count(start=1)

def load_counter_state():
    try:
        if os.path.exists(COUNTER_STATE_FILE):
            with open(COUNTER_STATE_FILE, 'r') as file:
                state = json.load(file)
                return state.get('feature_list_id', 1), state.get('proposal_id', 1)
        else:
            return 1, 1
    except json.JSONDecodeError:
        # Return default values if JSON is invalid or file is empty
        return 1, 1

def save_counter_state(feature_list_id, proposal_id):
    with open(COUNTER_STATE_FILE, 'w') as file:
        json.dump({'feature_list_id': feature_list_id, 'proposal_id': proposal_id}, file)


def process_initial_input(User_Vision):
    print("Simplifying initial input to focus on core functionalities...")
    system_context = "You are a Project Manager with expertise in lean and agile methodologies. Your task is to distill a user's vision into its most fundamental elements, focusing on the MVP."
    assistant_context = "Rules: Use maximum 500 words. Focus on identifying and refining the core elements of the vision. Avoid adding any complexities that are not crucial for the MVP."
    initial_prompt = f"Refine this user vision to its core elements, ensuring it aligns with MVP principles: {User_Vision}. Generate questions that could help in clarifying and focusing the vision."

    Vision_And_Questions = generate_text(system_context, assistant_context, initial_prompt)
    return Vision_And_Questions

def Answer_Questions(Vision_And_Questions):
    print("Answering questions to refine and focus the vision...")
    system_context = "You are a Product Manager with a knack for simplifying product concepts to their essence. You have a set of clarifying questions to refine a vision."
    assistant_context = "Rules: Use maximum 500 words. Your answers should focus on simplifying and clarifying the vision, aligning it with the MVP approach."
    initial_prompt = f"Provide answers to refine the vision towards an MVP: {Vision_And_Questions}"

    Answered_Questions = generate_text(system_context, assistant_context, initial_prompt)
    return Answered_Questions
def refine_vision(User_Vision, Vision_And_Questions, Answered_Questions):
    print("Crafting a streamlined and MVP-focused final vision...")
    system_context = "You are a Senior Visionary skilled in crafting clear, actionable, and lean visions for software projects, focusing on MVP development."
    assistant_context = "Rules: Use maximum 500 words. Create a final vision that is clear, streamlined, and focused on the MVP. Avoid complexities that don't align with the MVP approach."
    initial_prompt = f"Develop a final vision for an MVP based on the initial input: {User_Vision}, refined ideas: {Vision_And_Questions}, and answers: {Answered_Questions}. Keep the focus on essential MVP functionalities."

    Final_Vision = generate_text(system_context, assistant_context, initial_prompt)
    return Final_Vision

def identify_features(Final_Vision):
    print("Identifying essential features for the MVP...")
    system_context = f"You're an expert Python programmer with experience in software architecture, tasked with identifying features essential for an MVP based on the refined vision: {Final_Vision}."
    assistant_context = "Rules: Use a maximum of 2000 words. Identify only the core features and their critical sub-features that are essential for the MVP. Exclude supplementary features."
    initial_prompt = f"List the core features and crucial sub-features that are indispensable for the MVP, based on the refined vision: {Final_Vision}. Focus on functionalities essential for MVP operation."

    key_features_response = generate_text(system_context, assistant_context, initial_prompt)
    return key_features_response

def QualityCheckFeatures(Initial_Vision, key_features_response):
    print("Refining feature list for MVP alignment with initial vision...")
    system_context = "You're an AI Analyst with expertise in MVP development. Your task is to refine a list of proposed features against a project's initial vision to ensure they align with MVP principles."
    assistant_context = "Rules: Use a maximum of 2000 words. Focus solely on filtering out non-essential features. The output should list only the essential features that are critical for the MVP as per the initial vision."
    initial_prompt = f"Refine the proposed feature list to align with the MVP focus of the initial vision: {Initial_Vision}. The output should directly list the essential features and subfeatures and the subfeatures tasks without any additional summaries: {key_features_response}. Clearly identify the Feature, Sybfeatures and Tasks for processing into a json database format"

    refined_features_response = generate_text(system_context, assistant_context, initial_prompt)
    return refined_features_response
def List_Processor(refined_features_response):
    print("Formatting the features list...")
    system_context = "You're an AI specializing in data structuring and organization. Your task is to convert a list of key features, sub-features, and tasks into a structured JSON format suitable for software development project management. The output should be in a form that can be normalized for database storage and complexity analysis."
    assistant_context = "Rules: Use clear and unambiguous language. Organize the data so that each main feature is a key in the JSON object, with its sub-features as nested dictionaries. Each sub-feature should have associated tasks, each task should have a description, and where applicable, a task name. Ensure keys are easily readable and correspond to 'Feature', 'SubFeature', 'TaskName', and 'TaskDescription'."
    initial_prompt = f"Convert the provided list of key features, their sub-features, and associated tasks into a structured JSON object. Ensure that each feature is a key, with sub-features as nested dictionaries. Each sub-feature's tasks should be clearly listed with a description, and a task name. The structure should facilitate direct calls to features, sub-features, and task details for database normalization and analysis. Here is the list of features, sub-features, and tasks: {refined_features_response}"

    Structured_List = generate_list(system_context, assistant_context, initial_prompt)
    return Structured_List

def save_features_as_json1(structured_list):
    print("Saving features as JSON...")

    try:
        # Remove the non-JSON part of the string (if any)
        structured_list = structured_list.split("```json\n")[1]
        structured_list = structured_list.split("\n```")[0]

        # Convert the string to a Python dictionary
        feature_dict = json.loads(structured_list)

        # Save the dictionary as JSON
        with open('storage/FeatureList.json', 'w') as file:
            json.dump(feature_dict, file, indent=4)

        print("Features saved successfully.")
    except (json.JSONDecodeError, ValueError, IndexError) as e:
        print(f"Failed to process JSON. Error: {e}")
def normalize_features_for_database(feature_list_json):
    normalized_data = []

    # Check if the input is in the expected dictionary format with 'features' key
    if 'features' in feature_list_json:
        # Process the new format
        for feature_entry in feature_list_json['features']:
            feature_name = feature_entry.get("feature", "")
            for sub_feature_entry in feature_entry.get("subFeatures", []):
                sub_feature_name = sub_feature_entry.get("subFeature", "")
                for task in sub_feature_entry.get("tasks", []):
                    task_name = task.get("taskName", "")
                    task_description = task.get("taskDescription", "")
                    # Append the structured data
                    normalized_data.append({
                        "Feature": feature_name,
                        "SubFeature": sub_feature_name,
                        "TaskName": task_name,
                        "TaskDescription": task_description
                    })
    else:
        # Process the original format
        for feature, sub_features in feature_list_json.items():
            for sub_feature, sub_feature_data in sub_features.items():
                if isinstance(sub_feature_data, dict) and 'Tasks' in sub_feature_data:
                    for task in sub_feature_data['Tasks']:
                        normalized_data.append({
                            "Feature": feature,
                            "SubFeature": sub_feature,
                            "TaskName": task.get("TaskName", ""),
                            "TaskDescription": task.get("TaskDescription", "")
                        })
                else:
                    # Handle the scenario where tasks are directly under sub-features
                    for task_key, task_data in sub_feature_data.items():
                        if isinstance(task_data, dict) and "TaskName" in task_data and "TaskDescription" in task_data:
                            normalized_data.append({
                                "Feature": feature,
                                "SubFeature": sub_feature,
                                "TaskName": task_data.get("TaskName", ""),
                                "TaskDescription": task_data.get("TaskDescription", "")
                            })

    return normalized_data


def save_structured_data_as_json(structured_data, filename='FeatureListDatabase.json'):
    try:
        with open(filename, 'w') as file:
            json.dump(structured_data, file, indent=4)
        print(f"Structured data saved successfully in {filename}.")
    except Exception as e:
        print(f"Failed to save structured data as JSON. Error: {e}")


def save_features_as_json2(structured_data, proposal_id, feature_list_id, filename='storage/FeatureListDatabase.json'):
    # Update structured data with ProposalID and FeatureListID
    for feature in structured_data:
        feature['ProposalID'] = proposal_id
        feature['FeatureListID'] = feature_list_id

    try:
        # Load existing feature lists if file exists
        try:
            with open(filename, 'r') as file:
                feature_lists = json.load(file)
        except FileNotFoundError:
            feature_lists = []

        # Append the new feature list
        feature_lists.append({'FeatureListID': feature_list_id, 'Features': structured_data})

        # Save the updated feature lists
        with open(filename, 'w') as file:
            json.dump(feature_lists, file, indent=4)

        print(f"Feature list saved successfully in {filename} with ID: {feature_list_id}")
        save_counter_state(feature_list_id + 1, proposal_id + 1)  # Update both feature_list_id and proposal_id
        return feature_list_id
    except Exception as e:
        print(f"Failed to save feature list as JSON. Error: {e}")
        return None

def save_proposal(user_vision, final_vision, feature_list_id, proposal_id, filename='storage/Proposals.json'):
    new_proposal = {
        "ProposalID": proposal_id,
        "UserVision": user_vision,
        "FinalVision": final_vision,
        "FeatureListID": feature_list_id
    }

    try:
        # Load existing proposals if file exists
        proposals = []
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                proposals = json.load(file)

        # Add the new proposal
        proposals.append(new_proposal)

        # Save the updated proposals
        with open(filename, 'w') as file:
            json.dump(proposals, file, indent=4)
        print(f"Proposal saved successfully with ID: {proposal_id}")

    except Exception as e:
        print(f"Failed to save proposal. Error: {e}")


def main():
    feature_list_id_start, proposal_id_start = load_counter_state()
    global feature_list_id_counter, proposal_id_counter
    feature_list_id_counter = itertools.count(start=feature_list_id_start)
    proposal_id_counter = itertools.count(start=proposal_id_start)

    user_vision = input("Please enter your vision for the software project: ")
    print("Initializing Vision Processor...")

    Vision_And_Questions = process_initial_input(user_vision)
    Answered_Questions = Answer_Questions(Vision_And_Questions)
    Final_Vision = refine_vision(user_vision, Vision_And_Questions, Answered_Questions)
    key_features_response = identify_features(Final_Vision)
    refined_features_response = QualityCheckFeatures(user_vision, key_features_response)

    # Generate IDs at the start
    proposal_id = next(proposal_id_counter)
    feature_list_id = next(feature_list_id_counter)

    Structured_List = List_Processor(refined_features_response)

    # Save the initial feature list as FeatureList.json
    save_features_as_json1(Structured_List)

    # Check if 'FeatureList.json' was created
    try:
        with open('storage/FeatureList.json', 'r') as file:
            feature_list_json = json.load(file)
    except FileNotFoundError:
        print("'FeatureList.json' not found. Please check the feature list generation process.")
        return  # Exit the function if the file is

    # Normalize the features for the database
    structured_data = normalize_features_for_database(feature_list_json)
    save_features_as_json2(structured_data, proposal_id, feature_list_id)

    if feature_list_id is not None:
        save_proposal(user_vision, Final_Vision, feature_list_id, proposal_id)

        # Update the counter state at the end
    save_counter_state(next(feature_list_id_counter), next(proposal_id_counter))

    print("Process completed. Check 'FeatureList.json', 'FeatureListDatabase.json', and 'Proposals.json' for results.")


if __name__ == "__main__":
    main()