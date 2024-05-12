from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Path to the Complexity.json file
COMPLEXITY_FILE_PATH = os.path.join(app.root_path, 'storage', 'Complexity.json')

@app.route('/')
def index():
    with open(COMPLEXITY_FILE_PATH, 'r') as file:
        complexities = json.load(file)
    return render_template('ComplexityInput.html', complexities=complexities)

@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    # Validate that the hourly rate is an integer
    try:
        if 'Hourly Rate' in data:
            data['Hourly Rate']['Rate'] = int(data['Hourly Rate']['Rate'])
    except ValueError:
        return jsonify({"status": "error", "message": "Hourly rate must be an integer"}), 400
    with open(COMPLEXITY_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)
    return jsonify({"status": "success", "message": "Data saved successfully"})

if __name__ == '__main__':
    app.run(debug=True)