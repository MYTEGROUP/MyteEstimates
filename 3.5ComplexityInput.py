from flask import Flask, render_template, request, jsonify
import json
import os
from dotenv import load_dotenv
from tools.JsonOperators import get_base_path

app = Flask(__name__)

def get_storage_dir():
    base_path = get_base_path()
    load_dotenv(os.path.join(base_path, '.env'))
    storage_dir = os.getenv('MYTE_STORAGE_DIR', 'storage')
    return os.path.join(base_path, storage_dir)

# Path to the Complexity.json file
COMPLEXITY_FILE_PATH = os.path.join(get_storage_dir(), 'Complexity.json')


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
