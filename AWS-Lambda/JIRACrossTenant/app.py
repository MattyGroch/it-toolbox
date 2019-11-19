from chalice import Chalice
import os
import requests
from jira import Issue

app = Chalice(app_name='JIRACrossTenant')
# set to True if debugging
app.debug = False


@app.route('/', methods=['POST'])
def index():
    payload = app.current_request.json_body
    issue = Issue(payload)
