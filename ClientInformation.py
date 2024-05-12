from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Regexp
import json
import os
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Path to the JSON file where the data will be stored
JSON_FILE_PATH = os.path.join(os.getcwd(), 'Proposals.json')


class ClientForm(FlaskForm):
    companyName = StringField('Company Name', validators=[DataRequired()])
    contactPerson = StringField('Contact Person', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])  # Implement address search/validation externally
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Regexp(r'\d{1}-\d{3}-\d{3}-\d{4}')])
    website = StringField('Website', validators=[DataRequired()])  # Validate via external tool if needed
    submit = SubmitField('Save Information')


@app.route('/', methods=['GET', 'POST'])
def client_information():
    form = ClientForm()
    if form.validate_on_submit():
        client_info = {
            "CompanyName": form.companyName.data,
            "ContactPerson": form.contactPerson.data,
            "Address": form.address.data,
            "Email": form.email.data,
            "Phone": form.phone.data,
            "Website": form.website.data
        }

        # Load existing data or initialize new
        if os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, 'r') as file:
                data = json.load(file)
                data['ClientInformation'] = client_info
        else:
            data = {"ClientInformation": client_info}

        # Save the updated data back to the file
        with open(JSON_FILE_PATH, 'w') as file:
            json.dump(data, file, indent=4)

        return redirect(url_for('client_information'))

    return render_template('ClientInformation.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, port= 5005)
