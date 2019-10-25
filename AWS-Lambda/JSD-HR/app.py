from chalice import Chalice
import os
import json
import requests
import functions as fn
from jira import Issue, Employee

app = Chalice(app_name='JSD-HR')
# set to True if debugging
app.debug = False


@app.route('/', methods=['POST'])
def index():
    payload = app.current_request.json_body
    issue = Issue(payload)
    employee = Employee(payload)

    if issue.type == "New Hire":
        try:
            fn.onboard_user(issue, employee)
            return {'status': "Onboarding succe$ss."}
        except:
            return {'status': "An error ocurred with onboarding."}
    elif issue.type == "Termination":
        try:
            fn.terminate_user(issue, employee)
            return {'status': "Termination success."}
        except:
            return {'status': "An error ocurred with termination."}
    elif issue.type == "Change":
        try:
            fn.change_user(issue, employee)
            return {'status': "Information change success."}
        except:
            return {'status': "An error ocurred with information change."}
    else:
        return {'status': "Unknown issue type."}
