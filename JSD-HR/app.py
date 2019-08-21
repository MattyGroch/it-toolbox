from chalice import Chalice
import os
import json
import requests
import functions

app = Chalice(app_name='JSD-HR')
# set to True if debugging
app.debug = False

class JiraIssue:
    def __init__(self, request):
        self.id = request['issue']['id']
        self.key = request['issue']['key']
        self.priority = request['issue']['fields']['priority']['name']
        self.creator_username = request['issue']['fields']['creator']['name']
        self.creator_displayname = request['issue']['fields']['creator']['displayName']
        self.reporter_username = request['issue']['fields']['reporter']['name']
        self.reporter_displayname = request['issue']['fields']['reporter']['displayName']
        self.type = request['issue']['fields']['issuetype']['name']
        self.project = request['issue']['fields']['project']['key']
        self.summary = request['issue']['fields']['summary']
        self.description = request['issue']['fields']['description']


class Employee:
    def __init__(self, request):
        fields = request['issue']['fields']
        self.wage_type = fields['customfield_10161']['value']
        self.wage_amount = fields['customfield_10162']
        self.email = fields['customfield_10163']
        self.phone = fields['customfield_10164']
        self.flsa = fields['customfield_10165']['value']
        self.address1 = fields['customfield_10150']
        self.address2 = fields['customfield_10151']
        self.city = fields['customfield_10152']
        self.state = fields['customfield_10153']['value']
        self.zip = fields['customfield_10154']
        self.department = fields['customfield_10149']['value']
        self.firstname = fields['customfield_10142']
        self.lastname = fields['customfield_10143']
        self.preferredname = fields['customfield_10144']
        self.manager = fields['customfield_10145']['displayName']
        self.location = fields['customfield_10146']['value']


@app.route('/onboard', methods=['POST'])
def index():
    try:
        payload = app.current_request.json_body
        issue = JiraIssue(payload)
        employee = Employee(payload)
        functions.send_email("helpdesk@snapsheet.me",functions.generate_email("it"))
        functions.send_email("payroll@email.com",functions.generate_email("payroll"))
        return {'status': "Success."}
    except:
        return {'status': "An error ocurred."}


@app.route('/offboard', methods=['POST'])
def index():
    try:
        return {'status': "Not setup."}
    except:
        return {'status': "An error ocurred."}


@app.route('/infochange', methods=['POST'])
def index():
    try:
        return {'status': "Not setup."}
    except:
        return {'status': "An error ocurred."}
