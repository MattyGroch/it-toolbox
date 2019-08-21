from chalice import Chalice
import os
import json
import requests
import functions

app = Chalice(app_name='JSD-HR')
# set to True if debugging
app.debug = False

class JiraIssue:
    def __init__(self, payload):
        issue = payload['issue']
        self.id = issue['id']
        self.key = issue['key']
        self.priority = issue['fields']['priority']['name']
        self.creator_username = issue['fields']['creator']['name']
        self.creator_displayname = issue['fields']['creator']['displayName']
        self.reporter_username = issue['fields']['reporter']['name']
        self.reporter_displayname = issue['fields']['reporter']['displayName']
        self.type = issue['fields']['issuetype']['name']
        self.project = issue['fields']['project']['key']
        self.summary = issue['fields']['summary']
        self.description = issue['fields']['description']


class Employee:
    def __init__(self, payload):
        fields = payload['issue']['fields']
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
        functions.send_email("matt.grochocinski@gmail.com",functions.generate_email("employee"))
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
