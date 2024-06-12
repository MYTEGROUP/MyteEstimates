from datetime import datetime
from OpenAIModels.textgen import generate_text, generate_text_json
import json
from datetime import datetime


def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def write_json(data_str, file_path):
    # Convert the string formatted as JSON to a Python dictionary
    data = json.loads(data_str)

    # Write the dictionary to the JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def update_client_information(file_path, client_info):
    with open(file_path, 'r+') as file:
        data = json.load(file)
        data['ClientInformation'] = client_info
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()


def add_current_date_to_proposal(file_path):
    # Read the existing data from the file
    with open(file_path, 'r+') as file:
        data = json.load(file)

        # Get current date and format it
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Update or add the 'Date' key in the dictionary
        data['Date'] = {"CurrentDate": current_date}

        # Write the updated data back to the file
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

def update_user_information(file_path, user_info):
    with open(file_path, 'r+') as file:
        data = json.load(file)
        data['UserInformation'] = user_info
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

def update_our_qualifications(file_path, qualifications):
    with open(file_path, 'r+') as file:
        data = json.load(file)
        data['OurQualifications'] = qualifications
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
def ProposalCreateDetails(ProjectBreakdown, ProjectRequirements):
    print("Creating Proposal Information")

    jsonformat = """
    {
        "ProjectTitle": "Maximum 3 Words",
        "ExecutiveSummary": "",
        "Background": "",
        "Objectives": [
            "Objective 1",
            "Objective 2",
            "Objective X..."
        ],
        "Scope": "",
        "Deliverables": [
            "Deliverable 1",
            "Deliverable 2",
            "Deliverable X..."
        ]
    }
    """

    system_context = (
        "You're the Product Architect and you receive the Project Breakdown of epics stories and tasks, "
        "as well as the project requirements. You Create a ProjectTitle, ExecutiveSummary, Background, Objectives, Scope, Deliverables. "
        "You be detailed, and use simple high school level. It should be fun to read. You must ENSURE that every detail is represented from the ProjectBreakdown and ProjectRequirements.")
    assistant_context = f"Respond in json format like this: {jsonformat} :"
    initial_prompt = f"Here are the project Epics, Stories, and Tasks: {ProjectBreakdown} and the project requirements: {ProjectRequirements}. Please provide the ProjectTitle, ExecutiveSummary, Background, Objectives, Scope, Deliverables in the format instructed."

    projectdetails = generate_text_json(system_context, assistant_context, initial_prompt)
    print(f"{projectdetails}")
    return projectdetails


def ProposalMilestones(ProjectBreakdown, ProjectRequirements,GlobalDeliverables):
    print("Creating Proposal Milestones")

    jsonformat = """
    "Milestones": [
        {
          "MilestoneID": "",
          "MilestoneName": "",
          "KeyDeliverables": [
            "Deliverable 1",
            "Deliverable 2",
            "Deliverable 3"
          ]
        }
      ]
    """

    system_context = (
        "You're the Product Architect and you receive the Project Breakdown of epics stories and tasks, "
        "as well as the project requirements. You Create the Project Milestones and Deliverables inspired by the project deliverables established."
        "You be detailed, and use simple high school level. You must ENSURE that every detail is represented from the ProjectBreakdown and ProjectRequirements.")
    assistant_context = f"Respond in json format like this: {jsonformat} :"
    initial_prompt = f"Here are the project Epics, Stories, and Tasks: {ProjectBreakdown} and the project requirements: {ProjectRequirements}. We have Evaluated these Global Deliverables {GlobalDeliverables}. Provide your response per your instructions and in the format instructed. Limit yourself to 4 Milestones."

    milestones = generate_text_json(system_context, assistant_context, initial_prompt)
    print(f"{milestones}")
    return milestones

def ProposalRisks(ProjectBreakdown, ProjectRequirements):
    print("Creating Proposal Risks")

    jsonformat = """
       "Risks": [
            {
              "RiskID": "",
              "RiskDescription": "",
              "MitigationStrategies": [
                "Strategy 1",
                "Strategy 2",
                "Strategy 3"
              ]
            }
          ]
    """

    system_context = (
        "You're the Product Architect and you receive the Project Breakdown of epics stories and tasks, "
        "as well as the project requirements. You Create the Project Risks and Mitigation Strategies."
        "You be detailed, and use simple high school level - it is important to be aware of any major Risks and how we address them.")
    assistant_context = f"Respond in json format like this: {jsonformat} :"
    initial_prompt = f"Here are the project Epics, Stories, and Tasks: {ProjectBreakdown} and the project requirements: {ProjectRequirements}. Provide your response per your instructions and in the format instructed. Limit yourself to 3 Risks."

    risks = generate_text_json(system_context, assistant_context, initial_prompt)
    print(f"{risks}")
    return risks


def calculate_costs_and_hours(project_breakdown):
    total_hours = 0
    total_cost = 0
    cost_breakdown = []

    # Iterate over each stakeholder and their epics
    for stakeholder, epics in project_breakdown.items():
        stakeholder_details = {"Stakeholder": stakeholder, "Details": []}

        # Iterate over each epic and its stories
        for epic_id, stories in epics.items():
            epic_hours = 0
            epic_cost = 0
            epic_description = ""

            # Process each story in the epic
            for story in stories:
                story_hours = sum(task['Estimated Hours'] for task in story['Tasks'])
                story_cost = sum(task['Cost'] for task in story['Tasks'])
                if not epic_description:  # Assume all stories share the same epic description
                    epic_description = story['Epic Description']
                epic_hours += story_hours
                epic_cost += story_cost

            stakeholder_details['Details'].append({
                "Item": stories[0]['Epic Title'],  # Assuming the first story's title represents the epic
                "TotalHours": epic_hours,
                "Cost": epic_cost,
                "Description": epic_description
            })

            total_hours += epic_hours
            total_cost += epic_cost

        cost_breakdown.append(stakeholder_details)

    return total_hours, total_cost, cost_breakdown


def update_proposal_json(breakdown_file_path, proposal_file_path):
    project_breakdown = read_json(breakdown_file_path)
    proposal_data = read_json(proposal_file_path)

    total_hours, total_cost, cost_breakdown = calculate_costs_and_hours(project_breakdown)

    # Ensure the 'Budget' key exists in the proposal data and create it if not
    if 'Budget' not in proposal_data:
        proposal_data['Budget'] = {}

    proposal_data['Budget']['TotalEstimatedHours'] = total_hours
    proposal_data['Budget']['TotalEstimatedCost'] = total_cost
    proposal_data['Budget']['CostBreakdown'] = cost_breakdown

    # Write the updated data back to the JSON file
    with open(proposal_file_path, 'w') as file:
        json.dump(proposal_data, file, indent=4)

def add_proposal_id_to_json(file_path, proposal_id):
    # Read the existing data from the file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Add the Proposal ID to the data
    data['ProposalID'] = proposal_id

    # Write the updated data back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
def main():

    # Read contents of ProjectBreakdown1.json and Project_Requirements.json
    project_breakdown = read_json('storage/ProjectBreakdown1.json')
    project_requirements = read_json('storage/Project_Requirements.json')

    # Pass the contents to ProposalCreateDetails function
    project_details = ProposalCreateDetails(project_breakdown, project_requirements)

    # Save project details into Proposal.json
    write_json(project_details, 'storage/Proposal.json')

    # Extract global deliverables from Proposal.json
    proposal_data = read_json('storage/Proposal.json')
    global_deliverables = proposal_data.get('Deliverables', [])
    # Generate and update milestones
    proposal_milestones = ProposalMilestones(project_breakdown, project_requirements, global_deliverables)
    proposal_data['Milestones'] = json.loads(proposal_milestones)  # Assuming ProposalMilestones returns a JSON string

    # Generate and update Risks
    proposal_risks = ProposalRisks(project_breakdown, project_requirements)
    proposal_data['Risks'] = json.loads(proposal_risks)            # Assuming returns a JSON string

    # Write the updated proposal data back to the Proposal.json file
    with open('storage/Proposal.json', 'w') as file:
        json.dump(proposal_data, file, indent=4)

    ### Link this to a CRM of Clients
    client_info = {
        "CompanyName": "Confidential",
        "ContactPerson": "Confidential",
        "Address": "Confidential",
        "Email": "Confidential",
        "Phone": "Confidential"
    }

    #Link this to a CRM of Users of the Tool.
    user_info = {
        "CompanyName": "Myte Group Inc.",
        "Address": "7501 M.B Jodoin, Anjou, ",
        "Email": "ahmed.mekallach@mytegroup.com",
        "Phone": "5148049207",
        "Website": "www.mytegroup.com"
    }

    #Create a UI to capture this information from the user
    qualifications = {
        "CompanyProfile": "At Myte, we specialize in crafting custom AI automation solutions that streamline workflows and enhance operational efficiency for businesses across various industries. Our expertise lies in developing AI-powered websites and digital work environments tailored to the unique needs of our clients. By integrating artificial intelligence into core business processes, we deliver systems that not only reduce manual effort but also significantly increase accuracy and decision-making speed. Our commitment to innovation and excellence empowers businesses to achieve sustainable growth and maintain a competitive edge in their respective markets.",
        "RelevantExperience": "Myte Group has extensively optimized various internal operations through customized AI-driven solutions, particularly in sales, marketing, outreach, estimation, planning, and research. This expertise reflects our ability to enhance process efficiencies and accuracy, thereby improving time management and resource allocation across departments. Our strategic implementations of AI have significantly streamlined these key business functions, demonstrating our capability to elevate organizational performance and drive substantial growth through innovation in AI technology.",
        "TeamExpertise": "Under the leadership of Ahmed Mekallach, Myte Group boasts a profound expertise uniquely blending business acumen with technical prowess. With over eight years of experience in sales, estimating, and project management, Ahmed's comprehensive understanding of business processes and keen coding skills enable him to tackle challenges efficiently and innovatively. His approach not only ensures operational excellence but also drives the development of AI-driven solutions that are both sophisticated and practical, perfectly suited to meet the intricate demands of modern businesses. This unique combination positions Myte Group as a leader in AI systems design and development, capable of delivering high-quality, customized solutions."
    }

    file_path = 'storage/Proposal.json'
    update_client_information(file_path, client_info)
    update_user_information(file_path, user_info)
    update_our_qualifications(file_path, qualifications)


    update_proposal_json('storage/ProjectBreakdown1.json', 'storage/Proposal.json')
    add_current_date_to_proposal(file_path)
    # Add Proposal ID to Proposal.json
    proposal_id = "S2024016"  # Example hardcoded Proposal ID
    add_proposal_id_to_json('storage/Proposal.json', proposal_id)

if __name__ == "__main__":
    main()
