#7ReviewBreakdown.py
from flask import Flask, render_template, url_for, redirect, jsonify, request
import json

app = Flask(__name__)

# Global variable to hold the project data
project_data = {}

# Load the project data when the application starts, not as a before_first_request
with open('storage/ProjectBreakdown1.json') as file:
    project_data = json.load(file)
def save_changes():
    with open('storage/ProjectBreakdown1.json', 'w') as file:
        json.dump(project_data, file, indent=4)

@app.route('/')
def home():
    # Redirects to the first stakeholder as an entry point
    return redirect(url_for('stakeholder', name=list(project_data.keys())[0]))


@app.route('/stakeholder/<name>')
def stakeholder(name):
    if name not in project_data:
        return "Stakeholder not found", 404

    epics = project_data[name]  # Extracting the epics for the stakeholder
    stakeholders = list(project_data.keys())
    current_index = stakeholders.index(name)

    next_stakeholder = stakeholders[(current_index + 1) % len(stakeholders)]
    prev_stakeholder = stakeholders[(current_index - 1) % len(stakeholders)]

    return render_template('ApproveBreakdown.html', name=name, epics=epics,
                           next_stakeholder=next_stakeholder, prev_stakeholder=prev_stakeholder)

@app.route('/update', methods=['POST'])
def update_data():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': "No data provided"}), 400

    action = data['action']
    epic_id = data['epic_id']
    story_id = data.get('story_id')
    task_id = data.get('task_id')
    new_description = data.get('new_description', '')  # Assuming new description comes with the request

    try:
        found = False
        if 'delete' in action:
            # Delete actions
            for stakeholder, epics in project_data.items():
                if epic_id in epics:
                    if action == 'delete_epic':
                        del epics[epic_id]
                        found = True
                    elif action == 'delete_story':
                        epic = epics.get(epic_id)
                        if epic:
                            epic[:] = [story for story in epic if story['Story ID'] != story_id]
                            found = True
                    elif action == 'delete_task':
                        epic = epics.get(epic_id)
                        if epic:
                            for story in epic:
                                if story['Story ID'] == story_id:
                                    story['Tasks'] = [task for task in story['Tasks'] if task['Task ID'] != task_id]
                                    found = True
                                    break
                    break
            if not found:
                raise ValueError(f"Epic ID {epic_id} not found")
        else:
            # Approve actions
            for stakeholder, epics in project_data.items():
                if epic_id in epics:
                    epic = epics[epic_id]
                    for stakeholder, epics in project_data.items():
                        if epic_id in epics:
                            epic = epics[epic_id]
                            if action == 'approve_task':
                                for story in epic:
                                    if story['Story ID'] == story_id:
                                        for task in story['Tasks']:
                                            if task['Task ID'] == task_id:
                                                task['approved'] = True
                                                if new_description:
                                                    task['Description'] = new_description
                                                found = True
                                                break
                                        if found:
                                            break
                                if found:
                                    break
                            # Handle other actions (delete and approve story/epic)
                    if not found:
                        raise ValueError(f"Epic ID {epic_id} not found or Task/Story ID does not match")
                    elif action == 'approve_story':
                        story = next((story for story in epic if story['Story ID'] == story_id), None)
                        if not story:
                            raise ValueError(f"Story ID {story_id} not found")
                        if not all(task.get('approved', False) for task in story['Tasks']):
                            raise ValueError("Not all tasks in the story are approved")
                        story['approved'] = True
                        found = True
                    elif action == 'approve_epic':
                        if not all(story.get('approved', False) for story in epic):
                            raise ValueError("Not all stories in the epic are approved")
                        for story in epic:
                            story['approved'] = True
                        found = True
                    break
            if not found:
                raise ValueError(f"Epic ID {epic_id} not found")

        save_changes()
        return jsonify({'success': True})
    except Exception as e:
        app.logger.error(f"Error processing update: {str(e)}")  # Log the error
        return jsonify({'success': False, 'message': str(e)}), 500  # Return a JSON error response

if __name__ == '__main__':
    app.run(debug=True)