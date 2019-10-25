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
        print("New Hire ticket processing.")
        try:
            fn.onboard_user(issue, employee)
            return {'status': "Onboarding success."}
        except:
            return {'status': "An error ocurred with onboarding."}
    elif issue.type == "Termination":
        print("Termination ticket processing.")
        try:
            fn.terminate_user(issue, employee)
            return {'status': "Termination success."}
        except:
            return {'status': "An error ocurred with termination."}
    elif issue.type == "Change":
        print("Change ticket processing.")
        try:
            fn.change_user(issue, employee)
            return {'status': "Information change success."}
        except:
            return {'status': "An error ocurred with information change."}
    else:
        print("All conditions failed. No ticket processing.")
        return {'status': "Unknown issue type."}
