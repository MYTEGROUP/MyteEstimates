from OpenAIModels.textgen import generate_text, generate_text_json



def define_database_schema_list(task,story, acceptancecriteria, EpicGroup):
    print("Updating Authentication Schema...")
    system_context = (
        "You are a Software Product Database designer. You are tasked with defining the database schema based solely on the given task and the story/epic/stakeholder"
        "context this task is part of. You respond in JSON string format in the clearest structure possible."
    )
    assistant_context = (
        "Respond with in JSON string with a clear structure describing the data tables and columns necessary for the given task."
        "Include the necessary fields required for the completion of the given task. "
    )
    initial_prompt = ( f"Based solely on the Epic detailed breakdown : [{EpicGroup}], please define the database schema for"
                       f"this specific task : [{task}] within the story: [{story}] and the storys' acceptance criteria :[{acceptancecriteria}]. Respond in JSON format." )

    schema = generate_text_json(system_context, assistant_context, initial_prompt)

    with open('Brain/auth_schema.json', 'w') as file:
        file.write(schema)

def update_authentication_schema(task,story, acceptancecriteria, EpicGroup):
    print("Updating Authentication Schema...")
    system_context = (
        "You are a Software Product Database designer. You are tasked with defining the database schema based solely on the given task and the story/epic/stakeholder"
        "context this task is part of. You respond in JSON string format in the clearest structure possible."
    )
    assistant_context = (
        "Respond with in JSON string with a clear structure describing the data tables and columns necessary for the given task."
        "Include the necessary fields required for the completion of the given task. "
    )
    initial_prompt = ( f"Based solely on the Epic detailed breakdown : [{EpicGroup}], please define the database schema for"
                       f"this specific task : [{task}] within the story: [{story}] and the storys' acceptance criteria :[{acceptancecriteria}]. Respond in JSON format." )

    schema = generate_text_json(system_context, assistant_context, initial_prompt)

    with open('Brain/auth_schema.json', 'w') as file:
        file.write(schema)
    return schema


def update_api_endpoints(project_data):
    print("Creating API Endpoints...")
    system_context = (
        "Your task is to define the API endpoints for requesting and verifying OTPs as part of user authentication."
    )
    assistant_context = (
        "Respond with a JSON object detailing the API methods, URLs, and parameters necessary for the OTP request and verification processes."
    )
    initial_prompt = f"Based on the project data: {project_data}, define the API endpoints."

    api_endpoints = generate_text_json(system_context, assistant_context, initial_prompt)

    with open('Brain/api_endpoints.json', 'w') as file:
        file.write(api_endpoints)
    return api_endpoints


def update_integration_points(project_data):
    print("Specifying Integration Points...")
    system_context = (
        "As a system architect, identify the integration points for the new OTP authentication feature with existing systems such as session management and error handling."
    )
    assistant_context = (
        "Provide a JSON object that specifies how the OTP authentication integrates with other parts of the system. Include details on session creation, error handling, and logging."
    )
    initial_prompt = f"Using the following project information: {project_data}, outline the integration points."

    integration_points = generate_text_json(system_context, assistant_context, initial_prompt)

    with open('Brain/integration_points.json', 'w') as file:
        file.write(integration_points)
    return integration_points


def update_security_requirements(project_data):
    print("Defining Security Requirements...")
    system_context = (
        "You need to establish security requirements for the OTP authentication system, including protocols, encryption, and compliance standards."
    )
    assistant_context = (
        "Create a JSON object that defines security protocols for data transmission, encryption methods for sensitive data, and compliance with legal standards."
    )
    initial_prompt = f"Consider the following project specifics: {project_data}, and define the security requirements."

    security_requirements = generate_text_json(system_context, assistant_context, initial_prompt)

    with open('Brain/security_requirements.json', 'w') as file:
        file.write(security_requirements)
    return security_requirements
