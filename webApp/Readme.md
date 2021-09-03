# WEBSERVER USING FLASK
## Getting Started
### Dependencies
- python version 2.7 or greater (here i used Python 3.8.10)
- flask 2.0.1

### Installations 
- wsl2 
- make sure you are in your working directory, if not :
     ``` Bash
        > mkdir your_directory_name
        > cd your_directory_name  
       
- creating Virtual Environment: 
     ``` Bash
        > python3 -m venv venv
        > source venv/bin/activate
        > pip install -r requirements.txt 

- installing flask : 
     ``` Bash
        > pip install Flask

## Implementing Sendgrid
We use sendgrid to to deliver subscription email to the user.
refer to this site: https://app.sendgrid.com/guide/integrate
   ### STEPS:
   1. Sign In to Sendgrid using your official Mail ID.
   2. click here: https://app.sendgrid.com/guide/integrate 
   3. choose Python, it will navigate to the another page to create API key.
   4. follow all the steps mentioned there 
      - NOTE:
         - once you create your API Key make sure to save it anywhere for future reference,
            once you verify integrarion, you wont be able to copy your full API key.
   5. click on tick box in the bottom of the page and click on verify integration.
      - refer to sendgrid python documentation. https://github.com/sendgrid/sendgrid-python
      - make sure to change to settings of API key.
         1. go to setting> API keys> OR https://app.sendgrid.com/settings/api_keys
         2. there will be list of API keys you have created,  below actions, click on gear icon
         3. go to edit API Key
         4. Change the permissions to Full Access.
         5. drag down and click on update 
   
CODE:
``` Python
message = Mail(
    from_email ='your_domain_emailID@USEd _n_Sendgrid', #valid domain email verified by sendgrid
    to_emails = email,
    subject = 'Sending with Twilio SendGrid is Fun',
    html_content = '<strong>and easy to do anywhere, even with Python</strong>')
    try:
        s_g=SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = s_g.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
   ```
      
## Imports required
``` Python
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
```



### Test
use Debug Config Python: Flask\

## Reference 
- for error handling: https://www.geeksforgeeks.org/python-404-error-handling-in-flask/
- flask documentation: https://flask.palletsprojects.com/en/2.0.x/quickstart/
- python documentaion: https://docs.python.org/3/index.html
- http servers with python: https://docs.python.org/3/library/http.server.html
- JSON for Flask: https://pythonhosted.org/Flask-JSON/
- For doubts and other problems- 
    1. GITHUB- https://github.com/
    2. STACK OVERFLOW- https://stackoverflow.com/