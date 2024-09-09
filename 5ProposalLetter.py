from flask import Flask, render_template, make_response, request
from weasyprint import HTML, CSS
import io
import json
import os

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
    html = HTML(string=html_content, base_url=request.root_url)
    css = CSS(string='''
        @page { size: Letter; margin: 1in; }
        header, footer { position: fixed; width: 100%; }
        header { top: 0; margin-bottom: 50px; }
        footer { bottom: 0; text-align: center; margin-top: 50px; }
        .no-print { display: none; }
        body { margin-top: 200px; margin-bottom: 150px; } /* Adjust as needed */
        .footer-content p { margin: 5px 0; padding: 0; }
    ''')
    pdf = html.write_pdf(stylesheets=[css])

    # Save PDF to the Proposal directory
    proposal_directory = 'Proposal'
    if not os.path.exists(proposal_directory):
        os.makedirs(proposal_directory)

    pdf_filename = f"{proposal_directory}/{data['UserInformation']['CompanyName']} - {data['ProjectTitle']} - Proposal - {data['Date']['CurrentDate']}.pdf"
    with open(pdf_filename, 'wb') as pdf_file:
        pdf_file.write(pdf)

    # Create response
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=proposal.pdf'
    return response

if __name__ == "__main__":
    app.run(debug=True, port=9985)
