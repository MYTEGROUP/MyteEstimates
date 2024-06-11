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
    # Validate and convert hourly rates and complexity hours to floats
    try:
        if 'Hourly Rate' in data:
            data['Hourly Rate']['Rate'] = float(data['Hourly Rate']['Rate'])

        for key in data:
            if key != 'Hourly Rate':
                data[key]['hours'] = float(data[key]['hours'])
    except ValueError:
        return jsonify({"status": "error", "message": "Values must be numbers"}), 400

    with open(COMPLEXITY_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)

    return jsonify({"status": "success", "message": "Data saved successfully"})


if __name__ == '__main__':
    app.run(debug=True, port=1919)
