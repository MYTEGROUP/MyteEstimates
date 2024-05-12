from flask import Flask, render_template, make_response
from weasyprint import HTML
import io
import json

app = Flask(__name__)

def load_data():
    with open('storage/Proposal.json', 'r') as file:
        return json.load(file)

@app.route('/')
def index():
    data = load_data()
    return render_template('Proposal.html', data=data)

@app.route('/print_pdf', methods=['POST'])
def print_pdf():
    data = load_data()
    # Render HTML content
    html_content = render_template('Proposal.html', data=data)
    # Convert HTML to PDF
    html = HTML(string=html_content)
    pdf = html.write_pdf()

    # Create response
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=proposal.pdf'
    return response

if __name__ == "__main__":
    app.run(debug=True, port=9999)
