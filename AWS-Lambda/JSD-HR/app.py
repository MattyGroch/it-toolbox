from chalice import Chalice
import os
import json
import requests
import functions
import jira

app = Chalice(app_name='JSD-HR')
# set to True if debugging
app.debug = False


@app.route('/', methods=['POST'])
def index():
    payload = app.current_request.json_body
    issue = JiraIssue(payload)
    employee = Employee(payload)

    if issue.type == "New Hire":
        try:
            onboard_user(issue, employee)
            return {'status': "Onboarding success."}
        except:
            return {'status': "An error ocurred with onboarding."}
    elif issue.type == "Termination":
        try:
            terminate_user(issue, employee)
            return {'status': "Termination success."}
        except:
            return {'status': "An error ocurred with termination."}
    elif issue.type == "Change":
        try:
            change_user(issue, employee)
            return {'status': "Information change success."}
        except:
            return {'status': "An error ocurred with information change."}
    else:
        return {'status': "Unknown issue type."}
