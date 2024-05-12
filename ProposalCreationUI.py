from flask import Flask, render_template
import json

app = Flask(__name__)

def read_json(file_path):
    """Utility function to read a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

@app.route('/')
def index():
    proposal_data = read_json('storage/Proposal.json')
    project_breakdown = read_json('storage/ProjectBreakdown1.json')
    return render_template('Proposal.html', proposal_data=proposal_data, project_breakdown=project_breakdown)

if __name__ == '__main__':
    app.run(debug=True, port=9000)
