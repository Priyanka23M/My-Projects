from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from http import cookies
import os
from html import escape as html_escape
import cgi
import json
import logging
from urllib.parse import parse_qs
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import python_http_client.exceptions  #class for exceptions

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

form_inputs = cgi.FieldStorage()

FORM = '''<!DOCTYPE html>
<title>Subscriber Form</title>
<p>
{}
<p>
<form action = "/results" method = "POST">
<fieldset>
<label> Full name
<input type="text" name="fullname" /required>
</label>
<br>
<label> E Mail ID
<input type="email" name="email" /required>
</label>
<br>
<label>Phone Number
<input type="tel" name="phone_number">
</label>
<br>
<button type="submit">Subscribe!</button>
</fieldset>
</form>
'''
def storing_field_data_into_json_file( fullname, email, phone_number):
    form_data = []
    with open('formdata.txt', 'r') as outfile:
        try:
            form_data = json.load(outfile)
        except json.decoder.JSONDecodeError as priyanka:
            logger.error(priyanka)
        except TypeError as e_rror:
            logger.error(e_rror)
        
        else:
            pass 
    form_data.append(
        {
        "fullname": fullname,
        "email": email,
        "phone_number": phone_number
        }
    )
    with open('formdata.txt', 'w') as outfile:
        json.dump(form_data, outfile)

def sending_mail_with_sendgrid(email):
    message = Mail(
    from_email ='priyanka@omnispatial.xyz', #valid domain email verified by sendgrid
    to_emails = email,
    subject = 'Sending with Twilio SendGrid is Fun',
    html_content = '<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg=SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except python_http_client.exceptions.UnauthorizedError as e_rror: #Unauthirised error solved
        print(e_rror)
    except python_http_client.exceptions.ForbiddenError as e_rror: #forbidden error 403 solved
        print(e_rror.body)

class NameHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-length',0))
        data = self.rfile.read(length).decode()
        fullname = parse_qs(data)["fullname" ][0]
        email = parse_qs(data)["email"][0]
        phone_number = parse_qs(data)["phone_number"][0]

        cookie = self.saving_cookie(fullname, email, phone_number)
        
        self.send_response(303)
        self.send_header('Location', '/')
        self.send_header('Set-Cookie',cookie['fullname'].OutputString())
        self.send_header('Set-Cookie',cookie['email'].OutputString())
        self.send_header('Set-Cookie',cookie['phone_number'].OutputString())
        self.end_headers()

        #calling fuction to store field data
        storing_field_data_into_json_file(fullname, email, phone_number)

        #calling function to send mail to user via sendgrid API
        sending_mail_with_sendgrid(email)

    def saving_cookie(self, fullname, email, phone_number):
        cookie = cookies.SimpleCookie()
        cookie['fullname'] = fullname
        cookie['fullname']['domain'] = 'localhost'
        cookie['fullname']['max-age'] = 60
        cookie['email'] = email
        cookie['email']['domain'] = 'localhost'
        cookie['email']['max-age'] = 60
        cookie['phone_number'] = phone_number
        cookie['phone_number']['domain'] = 'localhost'
        cookie['phone_number']['max-age'] = 60
        return cookie
    def do_GET(self):
        message = "Hey Dont Miss our Updates! Subscribe now"
        if 'cookie' in self.headers:
            try:
                cookie=cookies.SimpleCookie(self.headers['cookie'])
                fullname=cookie['fullname'].value
                email=cookie['email'].value
                phone_number=cookie['phone_number'].value
                message="thanks for submitting" + html_escape(fullname)
                message="thanks for submitting " + html_escape(email)
                message="thanks for submitting " + html_escape(phone_number)
            except (KeyError, cookies.CookieError) as e_rror:
                message = "I'm not sure who you are!"
                print(e_rror)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        mesg=FORM.format(message)
        self.wfile.write(mesg.encode())

if __name__ == '__main__':
    port=int(os.environ.get('PORT',8001))
    server_address=('', port)
    httpd=ThreadingHTTPServer(server_address, NameHandler)
    httpd.serve_forever()
