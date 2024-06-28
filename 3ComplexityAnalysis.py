from OpenAIModels.textgen import generate_text, generate_text_json
import json
import os
import threading
from queue import Queue
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_complexity_hours(file_path):
    """
    Load the hours associated with each complexity level from Complexity.json.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def generate_task_complexity(task,tasks,story, epic, stakeholder):

    """
    Generate the complexity of a given task
    """
    complexityoptions = """
    
    {
    "Complexity Levels": [
        {
            "Level": "Very Simple",
            "Description": "Tasks that require minimal coding and can be completed quickly without much research or planning. Typically involves changes to a single area of the application.",
            "Examples": [
                "Updating the footer content on a website.",
                "Changing the color scheme of a webpage.",
                "Adding a new contact email address in the header.",
                "Replacing an old logo with a new one.",
                "Correcting typos in static text.",
                "Updating links in a navigation menu.",
                "Adding social media icons to a homepage.",
                "Creating a simple CSS class for text formatting.",
                "Adding a read-only field to a form.",
                "Removing a deprecated script from pages.",
                "Adding alt text to images for accessibility.",
                "Setting up a redirect for a discontinued page.",
                "Updating API keys in configuration files.",
                "Increasing the size of buttons on mobile views.",
                "Removing unused CSS styles.",
                "Adding a favicon to the site tab.",
                "Implementing a simple date display on the site.",
                "Adding a printer-friendly option to a page.",
                "Updating timezone settings for user display.",
                "Adding a basic page loading spinner."
            ]
        },
        {
            "Level": "Simple",
            "Description": "Tasks that require a bit more involvement than very simple tasks, often involving minor logic changes or updates that affect multiple files but not complex systems interactions.",
            "Examples": [
                "Updating user authentication logic to add an additional security question.",
                "Modifying the layout of a homepage to add a new section for monthly features.",
                "Creating a script to automatically convert uploaded images to a different format.",
                "Adding a sorting feature to the product listing page.",
                "Implementing pagination in a list that displays more than 50 items per page.",
                "Designing a new email template for marketing with placeholder values.",
                "Setting up a basic REST API endpoint to retrieve user data by ID.",
                "Writing a utility function to format dates across the site consistently.",
                "Adding a filter by date range on the transaction history page.",
                "Implementing a basic search function for the blog section of a website.",
                "Creating a user settings page that allows users to customize layout preferences.",
                "Adding functionality to a dashboard that lets users pin their favorite reports.",
                "Integrating a third-party API to send SMS notifications for system alerts.",
                "Developing a script to automatically deactivate users after one year of inactivity.",
                "Modifying an existing form to include validation checks before submission.",
                "Implementing error logging for failed login attempts.",
                "Creating a batch process to update user status based on monthly activity.",
                "Setting up a new module to handle user feedback through a simple form.",
                "Writing a script to check and repair broken links reported by users on the site.",
                "Adding multi-language support for the top 10 most visited pages of the site."
            ]
        },
        {
            "Level": "Medium",
            "Description": "Tasks that involve integrating multiple system components, moderate algorithmic complexity, or building new features with several steps.",
            "Examples": [
                "Integrating a new payment gateway that supports multiple currencies.",
                "Developing a feature for users to customize and export their data reports in various formats.",
                "Creating a dynamic form builder that allows users to create their own forms with validation rules.",
                "Building a multi-step user registration process that includes email verification and captcha.",
                "Designing and implementing a user role management system with different access levels.",
                "Implementing a recommendation engine that suggests products based on user behavior.",
                "Developing a real-time chat application that supports group chats and file sharing.",
                "Creating an automated job to synchronize data across different databases nightly.",
                "Building a dashboard that aggregates data from multiple sources and displays it in interactive charts.",
                "Developing a mobile-responsive layout for an existing web application.",
                "Integrating third-party API services to enhance existing features like geolocation mapping.",
                "Creating a version control system for document editing within a web application.",
                "Building a notification system that sends alerts based on user-defined triggers.",
                "Designing a custom algorithm to handle complex data sorting and filtering on a large dataset.",
                "Developing a feature that allows users to schedule and automate repetitive tasks within the application.",
                "Creating a backup system that performs incremental backups of user data and system settings.",
                "Implementing an audit trail system that logs all user activities and system changes.",
                "Designing a system to manage and rotate API keys and credentials securely.",
                "Developing a load balancing solution for a high-traffic web application.",
                "Implementing a complex security protocol to protect sensitive data transmissions within the system."
            ]
        },
        {
            "Level": "Complex",
            "Description": "Tasks that require advanced programming skills, extensive integration with multiple systems, or significant architectural changes.",
            "Examples": [
                "Developing a microservices architecture to handle different aspects of a large-scale e-commerce platform.",
                "Integrating a full-text search engine into an existing database with over a million records.",
                "Designing and implementing a distributed caching system to improve application performance.",
                "Creating a custom data encryption and decryption module to enhance security for sensitive user data.",
                "Building a complex event processing system to handle real-time analytics and data streaming.",
                "Implementing a multi-factor authentication system across various parts of an application.",
                "Developing an AI-based image recognition system to automatically tag and categorize user uploads.",
                "Creating a blockchain-based transaction system for secure and verifiable exchange of digital assets.",
                "Designing a robust error handling and recovery system for a critical financial processing application.",
                "Implementing a dynamic resource allocation system for a cloud-based hosting environment.",
                "Developing a predictive maintenance system for industrial machinery using IoT data.",
                "Creating an advanced natural language processing system to interpret and respond to customer inquiries.",
                "Designing a high-availability system architecture to ensure zero downtime for a mission-critical application.",
                "Implementing a real-time data synchronization system across multiple international locations.",
                "Building an intelligent routing system to optimize data flow within a network of distributed services.",
                "Developing a custom scripting language and runtime environment for automation tasks.",
                "Creating a detailed simulation environment to test new features under various operational conditions.",
                "Designing a cross-platform mobile application that integrates deeply with hardware features.",
                "Implementing a comprehensive audit and compliance tracking system for a regulated industry.",
                "Developing a sophisticated recommendation engine that adjusts in real-time based on user interactions."
            ]
        },
        {
            "Level": "Very Complex",
            "Description": "Tasks that involve cutting-edge technology, significant research and development, or complex integrations over multiple platforms and systems.",
            "Examples": [
                "Developing a decentralized autonomous organization (DAO) platform with smart contract functionality.",
                "Creating a real-time distributed machine learning platform for processing petabytes of data.",
                "Designing and implementing a full-fledged quantum computing simulation environment.",
                "Building a cross-continental disaster recovery system that synchronizes data across multiple data centers in real-time.",
                "Developing a deep neural network for processing and predicting outcomes based on genomic data.",
                "Creating an advanced AI-driven predictive analytics tool that integrates with multiple financial markets.",
                "Designing a highly secure digital voting system that can handle millions of concurrent users.",
                "Implementing a hybrid cloud infrastructure that seamlessly integrates with existing on-premise legacy systems.",
                "Developing a multi-tenant platform capable of hosting hundreds of independent instances with full isolation.",
                "Creating a complex augmented reality system that integrates with live data feeds for interactive user experiences.",
                "Building a fully automated, AI-powered supply chain management system that predicts and adjusts to market changes.",
                "Developing a high-frequency trading platform that uses advanced algorithms to trade across multiple exchanges.",
                "Creating a scalable blockchain-based data integrity system for a global logistics network.",
                "Designing a fault-tolerant control system for autonomous vehicles that operates under various environmental conditions.",
                "Implementing a secure, end-to-end encrypted communication platform for governmental use.",
                "Developing a serverless architecture that dynamically scales for millions of users without downtime.",
                "Creating an AI-based system for automated medical diagnosis using patient data across multiple health institutions.",
                "Building a sophisticated environmental monitoring system using satellite imaging and ground sensor data.",
                "Developing a virtual reality platform for immersive remote collaboration in engineering and design.",
                "Creating a complex algorithm for optimizing large-scale 3D printing processes in real-time."
            ]
        }
    ]
}

    
    
 
    """
    system_context = (f"You are a software business owner, evaluating complexity of a given task to code. You'll also be provided with the Story,Epic,Stakeholder the task is nested under for context."
                      f"Your response must be one of the following options: {complexityoptions}"
                      "Your response should be one of these options: [Very Simple, Simple, Medium, Complex, Very Complex]"
                      )
    assistant_context = ("You provide only the complexity as your response worded exactly as per your instruction, "
                         "in string format with no explanation before or after the complexity.")


    initial_prompt = (f"Given the tasks {tasks}, the Story: {story} the tasks are nested under, the Epic: {epic} the story is nested under, and the stakeholder : {stakeholder} the epic is nested under,"
                      f"evaluate the complexity of this task: {task}. Respond by providing one of the five complexity options given in your instructions.")
    Complexity = generate_text(system_context, assistant_context, initial_prompt)

    return Complexity

def update_complexity(all_tasks, task, index, story, epic, stakeholder, complexity_hours, hourly_rate):
    all_tasks_descriptions = [t['Description'] for t in all_tasks]
    complexity = generate_task_complexity(task['Description'], all_tasks_descriptions, story['Story Title'], epic['Epic Title'], stakeholder)
    task['Complexity'] = complexity
    task['Estimated Hours'] = complexity_hours[complexity]["hours"]
    task['Cost'] = task['Estimated Hours'] * hourly_rate  # Calculate cost based on hourly rate
    print(f"Task ID: {task.get('Task ID', 'Unknown ID')} - Complexity: {complexity}, Hours: {task['Estimated Hours']}, Cost: {task['Cost']}")
    return index, task, stakeholder, epic['Epic ID'], story['Story Index']

def worker():
    while True:
        item = q.get()
        if item is None:
            break
        all_tasks, task_data, index, story, epic, stakeholder = item
        updated_task = update_complexity(all_tasks, task_data, index, story, epic, stakeholder, complexity_hours, hourly_rate)
        results.append(updated_task)
        q.task_done()

def read_and_process_json(file_path, complexity_file_path):
    global complexity_hours, hourly_rate
    complexity_data = load_complexity_hours(complexity_file_path)
    complexity_hours = {k: v for k, v in complexity_data.items() if k != "Hourly Rate"}
    hourly_rate = complexity_data["Hourly Rate"]["Rate"]  # Retrieve the hourly rate

    with open(file_path, 'r') as file:
        data = json.load(file)

    threads = []
    num_worker_threads = 10

    for i in range(num_worker_threads):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    for stakeholder, epics in data.items():
        for epic_id, epic_data in epics.items():
            for story in epic_data:
                tasks = story['Tasks']
                for task_index, task in enumerate(tasks):
                    q.put((tasks, task, task_index, story, epic_data[0], stakeholder))

    q.join()

    for i in range(num_worker_threads):
        q.put(None)
    for t in threads:
        t.join()

    # Update the JSON data structure
    for result in results:
        index, task, stakeholder, epic_id, story_index = result
        data[stakeholder][epic_id][story_index]['Tasks'][index] = task

    # Save updated data back to JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def calculate_totals(file_path):
    """
    Calculate the total hours and total cost of the project from the JSON file.
    """
    total_hours = 0
    total_cost = 0

    # Load the JSON file with project data
    with open(file_path, 'r') as file:
        project_data = json.load(file)

    # Iterate through each stakeholder, epic, and task to sum hours and costs
    for stakeholder, epics in project_data.items():
        for epic_id, stories in epics.items():
            for story in stories:
                for task in story['Tasks']:
                    total_hours += task['Estimated Hours']
                    total_cost += task['Cost']

    # Print the total hours and total cost
    print(f"Total Hours: {total_hours}")
    print(f"Total Cost: ${total_cost}")

if __name__ == '__main__':
    results = []
    q = Queue()
    file_path = os.path.join('storage', 'ProjectBreakdown1.json')
    complexity_file_path = os.path.join('storage', 'Complexity.json')
    read_and_process_json(file_path, complexity_file_path)
    calculate_totals(file_path)