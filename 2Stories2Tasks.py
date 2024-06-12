#2Stories2Tasks.py
import json
from OpenAIModels.textgen import generate_text, generate_text_json
import threading
import queue
import time
from threading import Semaphore, Timer, Lock
from collections import OrderedDict

# Initialize semaphore with 60 permits
rate_limit_semaphore = Semaphore(30)

def reset_semaphore(timer):
    """
    Resets the semaphore back to its initial state every minute to manage rate limiting.
    """
    global rate_limit_semaphore
    with threading.Lock():
        rate_limit_semaphore = Semaphore(60)
    if timer and not timer.finished.is_set():
        timer = Timer(60, reset_semaphore, [timer])
        timer.start()

# def process_story(story_data, project_breakdown, all_tasks):
#     """
#     Processes each story to generate tasks based on the provided acceptance criteria and other details.
#     """
#     stakeholder, epic, story, index = story_data
#     tasks_json = generate_tasks_for_story(
#         story['Description'], story['AcceptanceCriteria'], epic['Description'], stakeholder, project_breakdown
#     )
#     tasks = json.loads(tasks_json)['Tasks']
#     all_tasks.append({
#         "Stakeholder": stakeholder,
#         "Epic ID": epic['Epic ID'],
#         "Epic Title": epic['Title'],
#         "Epic Description": epic['Description'],
#         "Story ID": story['Story ID'],
#         "Story Title": story['Title'],  # Include Story Title in the output
#         "Story Description": story['Description'],
#         "Story Acceptance Criteria": story['AcceptanceCriteria'],
#         "Tasks": tasks,
#         "Story Index": index
#     })
#
# def task_processor(task_queue, project_breakdown, all_tasks):
#     """
#     Thread function to process tasks from the queue.
#     """
#     while not task_queue.empty():
#         story_data = task_queue.get()
#         rate_limit_semaphore.acquire()
#         try:
#             process_story(story_data, project_breakdown, all_tasks)
#         finally:
#             task_queue.task_done()
#             rate_limit_semaphore.release()
#
# def generate_tasks_for_story(story, acceptance_criteria, epic, stakeholder,project_breakdown):
#
#     """
#     Generates detailed tasks for a given story in JSON format.
#     """
#
#     system_context = (
#         "As a Software Product Architect, your task is to decompose the user story and its acceptance criteria into detailed, actionable tasks suitable for a development team. "
#         "Provide tasks that are specific, measurable, achievable, and relevant that can be packaged into a function on python with clear inputs and outputs in the description. "
#         "Your response should be based specifically on the provided project context: the story, its acceptance criteria, the epic it's under, "
#         "the stakeholder the epic is under, the list of stakeholders, epics, stories. Do not provide a time estimate in the task description."
#         "Consider the following Tech Stack : (Python / Flask -- AWS services for databases -- OpenAI API For any NLP Transformer needs -- Desktop Application focus for Windows)"
#     )
#
#     assistant_context = ("Structure each task in a JSON format with key 'Tasks' and then a list of descriptions for each task. "
#                          "Follow this structure: {'Tasks': [{'Description': 'Task Description'},{'Description': 'Task Description'},{..},..]}")
#
#
#     initial_prompt = (
#         f"Given the project breakdown so far : [{project_breakdown}] ]"
#         f"Focused on stakeholder [{stakeholder}],epic [{epic}], story [{story}], and its acceptance criteria [{acceptance_criteria}]. "
#         "Decompose the story into actionable tasks that are SMART and align with the acceptance criteria. "
#         "Structure each task in a JSON format with key 'Description'. Do not provide a time estimate in the task description."
#     )
#     tasks = generate_text_json(system_context, assistant_context, initial_prompt)
#
#     return tasks

#without project_breakdown:
def process_story(story_data, all_tasks):
    """
    Processes each story to generate tasks based on the provided acceptance criteria and other details.
    """
    stakeholder, epic, story, index = story_data
    tasks_json = generate_tasks_for_story(
        story['Description'], story['AcceptanceCriteria'], epic['Description'], stakeholder)
    tasks = json.loads(tasks_json)['Tasks']
    all_tasks.append({
        "Stakeholder": stakeholder,
        "Epic ID": epic['Epic ID'],
        "Epic Title": epic['Title'],
        "Epic Description": epic['Description'],
        "Story ID": story['Story ID'],
        "Story Title": story['Title'],  # Include Story Title in the output
        "Story Description": story['Description'],
        "Story Acceptance Criteria": story['AcceptanceCriteria'],
        "Tasks": tasks,
        "Story Index": index
    })

def task_processor(task_queue, all_tasks):
    """
    Thread function to process tasks from the queue.
    """
    while not task_queue.empty():
        story_data = task_queue.get()
        rate_limit_semaphore.acquire()
        try:
            process_story(story_data, all_tasks)
        finally:
            task_queue.task_done()
            rate_limit_semaphore.release()

def generate_tasks_for_story(story, acceptance_criteria, epic, stakeholder):

    """
    Generates detailed tasks for a given story in JSON format.
    """

    system_context = (
        "As a Software Product Architect, your task is to decompose the user story and its acceptance criteria into detailed, actionable tasks suitable for a development team. "
        "Provide tasks that are specific, measurable, achievable, and relevant that can be packaged into a function on python with clear inputs and outputs in the description. "
        "Your response should be based specifically on the provided project context: the story, its acceptance criteria, the epic it's under, "
        "the stakeholder the epic is under, the list of stakeholders, epics, stories. Do not provide a time estimate in the task description."
        "Consider the following Tech Stack : (Python / Flask -- AWS services for databases -- OpenAI API For any NLP Transformer needs -- Desktop Application focus for Windows)"
    )

    assistant_context = ("Structure each task in a JSON format with key 'Tasks' and then a list of descriptions for each task. "
                         "Follow this structure: {'Tasks': [{'Description': 'Task Description'},{'Description': 'Task Description'},{..},..]}")


    initial_prompt = (
        f"Given the stakeholder [{stakeholder}],epic [{epic}], story [{story}], and acceptance criteria [{acceptance_criteria}], "
        "decompose the story into actionable tasks that are SMART and align with the acceptance criteria. "
        "Each task description should describe a functions inputs , transformation and outputs if any. "
        "Together, these functions accomplish specifically the requirements of the story for the epic/stakeholder."
        "Structure each task in a JSON format with key 'Description'. Do not provide a time estimate in the task description."
    )
    tasks = generate_text_json(system_context, assistant_context, initial_prompt)

    return tasks

def main():
    """
    Main function to orchestrate the task processing.
    """

    timer = Timer(60, reset_semaphore, [None])
    timer.start()

    with open('storage/ProjectBreakdown.json') as file:
        project_breakdown = json.load(file, object_pairs_hook=OrderedDict)

    task_queue = queue.Queue()
    all_tasks = []
    threads = []

    # Queue up all stories with their index for processing
    for stakeholder, epics in project_breakdown.items():
        for epic in epics:
            for index, story in enumerate(epic['User Stories']):
                print(f"Processing {epic['Title']}")
                task_queue.put((stakeholder, epic, story, index))

    # # Start threads to process tasks
    # for _ in range(10):  # Number of threads
    #     thread = threading.Thread(target=task_processor, args=(task_queue, project_breakdown, all_tasks))
    #     threads.append(thread)
    #     thread.start()

    # Start threads to process tasks
    for _ in range(10):  # Number of threads
        thread = threading.Thread(target=task_processor, args=(task_queue, all_tasks))
        threads.append(thread)
        thread.start()

    # Wait for all tasks to be processed
    task_queue.join()
    for thread in threads:
        thread.join()
    timer.cancel()

    # Structuring the collected data
    results = OrderedDict()
    for task_data in sorted(all_tasks, key=lambda x: (x['Stakeholder'], x['Epic ID'], x['Story Index'])):
        stakeholder = task_data['Stakeholder']
        epic_id = task_data['Epic ID']

        if stakeholder not in results:
            results[stakeholder] = OrderedDict()
        if epic_id not in results[stakeholder]:
            results[stakeholder][epic_id] = []

        results[stakeholder][epic_id].append(task_data)

    # Assigning Task IDs within each stakeholder
    for stakeholder, epics in results.items():
        task_counter = 1
        for epic_id, stories in epics.items():
            for story in stories:
                for task in story['Tasks']:
                    task['Task ID'] = f"T{task_counter:03d}"
                    task_counter += 1

    # Save results to JSON
    with open('storage/ProjectBreakdown1.json', 'w') as file:
        json.dump(results, file, indent=4)


if __name__ == "__main__":
    main()


