from chalice import Chalice
import os
import json
import requests
import functions

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
            return {'status': "Success."}
        except:
            return {'status': "An error ocurred."}
    elif issue.type == "Termination":
        try:
            terminate_user(issue, employee)
            return {'status': "Success."}
        except:
            return {'status': "An error ocurred."}
    elif issue.type == "Information Change":
        try:
            change_user(issue, employee)
            return {'status': "Success."}
        except:
            return {'status': "An error ocurred."}
    else:
        return {'status': "Unknown issue type."}
