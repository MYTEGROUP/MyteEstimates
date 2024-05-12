import json


def calculate_costs_and_hours(project_breakdown):
    total_hours = 0
    total_cost = 0
    cost_breakdown = []

    for stakeholder, epics in project_breakdown.items():
        stakeholder_details = {"Stakeholder": stakeholder, "Details": []}

        for epic_id, stories in epics.items():
            epic_hours = 0
            epic_cost = 0
            epic_description = stories[0]['Epic Description']  # Assuming the first story's description applies to the whole epic

            for story in stories:
                story_hours = sum(task['Estimated Hours'] for task in story['Tasks'])
                story_cost = sum(task['Cost'] for task in story['Tasks'])
                epic_hours += story_hours
                epic_cost += story_cost

            stakeholder_details['Details'].append({
                "Item": stories[0]['Epic Title'],
                "TotalHours": epic_hours,
                "Cost": epic_cost,
                "Description": epic_description
            })

            total_hours += epic_hours
            total_cost += epic_cost

        cost_breakdown.append(stakeholder_details)

    return total_hours, total_cost, cost_breakdown

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


project_breakdown = read_json('storage/ProjectBreakdown1.json')
total_hours, total_cost, cost_breakdown = calculate_costs_and_hours(project_breakdown)
print(f"{total_hours, total_cost, cost_breakdown}")