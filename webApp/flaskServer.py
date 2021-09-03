import os
import logging
import cgi
import json
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField
from wtforms.fields.simple import PasswordField
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import python_http_client.exceptions

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

form_inputs = cgi.FieldStorage()

app = Flask(__name__, template_folder='templates')
app.secret_key = 'user subscription form app'

# @app.errorhandler(404)
# def not_found(e_r):
#     return render_template("404.html")

class SubscriptionForm(FlaskForm):
    name = TextField("Name")
    email = TextField("Email")
    subject = TextField("Phone_number")
    password = PasswordField("password")
    submit = SubmitField("Send")

@app.route('/')
@app.route('/subscribeus', methods=["GET","POST"])

def index():

    form = render_template('index.html')

    if request.method=='POST':
        name =  request.form.get("name")
        email = request.form.get("email")
        phone_number = request.form.get("phone_number")
        password = request.form.get("password")
        result = []
        try:
            with open('formdata.txt', 'r') as outfile:
                try:
                    result = json.load(outfile)
                except json.decoder.JSONDecodeError as e_r:
                    app.logger.error(msg=e_r)
                except TypeError as e_rror:
                    app.logger.error(e_rror)

                else:
                    pass

             ###checking json key###
                for user_info in result:
                    if user_info ["email"]==email:
                        app.logger.info(f"user : {email} exits ")
                        return("user exists ", 200)
                    else:
                        writing_file(name, email, phone_number, password, result)
                        sending_mail_with_sendgrid(email)
                        return("user registered successfuly", 200)

        except FileNotFoundError as e_r:
            app.logger.error(e_r)
            app.logger.info("NO FILE IN DISK")
            writing_file(name, email, phone_number, password, result)

        return render_template('index.html', form=form)

    else:
        return render_template('index.html', form=form)

def writing_file(name, email, phone_number, password, result):
    result.append(
                        {
                    'name':name,
                    'email':email,
                    'phone_number': phone_number,
                    'password ': password
                    },
                    )
    with open('formdata.txt', 'w') as outfile:
        json.dump(result, outfile)
def sending_mail_with_sendgrid(email):
    message = Mail(
    from_email ='priyanka@omnispatial.xyz', #valid domain email verified by sendgrid
    to_emails = email,
    subject = 'Sending with Twilio SendGrid is Fun',
    html_content = '<strong>and easy to do anywhere, even with Python</strong>')
    try:
        s_g=SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = s_g.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except python_http_client.exceptions.UnauthorizedError as e_rror: #Unauthirised error solved
        print(e_rror)
    except python_http_client.exceptions.ForbiddenError as e_rror: #forbidden error 403 solved
        print(e_rror.body)

if __name__ == '__main__':
    app.run(debug = True)
    app.run(host='0.0.0.0', port=8000)
