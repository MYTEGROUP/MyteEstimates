#4ReviewBreakdown.py
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
    action = data['action']
    epic_id = data['epic_id']
    story_id = data.get('story_id')
    task_id = data.get('task_id')

    try:
        stakeholder = next((s for s in project_data.values() if epic_id in s), None)
        if not stakeholder:
            raise ValueError(f"Epic ID {epic_id} not found")

        epic = stakeholder[epic_id]
        if action == 'approve_task':
            story = next((story for story in epic if story['Story ID'] == story_id), None)
            if not story:
                raise ValueError(f"Story ID {story_id} not found in Epic ID {epic_id}")
            task = next((task for task in story['Tasks'] if task['Task ID'] == task_id), None)
            if not task:
                raise ValueError(f"Task ID {task_id} not found in Story ID {story_id}")
            task['approved'] = True
        elif action == 'approve_story':
            story = next((story for story in epic if story['Story ID'] == story_id), None)
            if not story:
                raise ValueError(f"Story ID {story_id} not found in Epic ID {epic_id}")
            if not all(task.get('approved', False) for task in story['Tasks']):
                raise ValueError(f"Not all tasks in Story ID {story_id} are approved")
            story['approved'] = True
        elif action == 'approve_epic':
            if not all(story.get('approved', False) for story in epic):
                raise ValueError(f"Not all stories in Epic ID {epic_id} are approved")
            for story in epic:
                story['approved'] = True
        else:
            raise ValueError('Invalid action')
        save_changes()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
