from chalice import Chalice
import os
import json
import requests
import functions

app = Chalice(app_name='JSD-HR')
# set to True if debugging
app.debug = False


@app.route('/onboard/{issue}', methods=['POST'])
def index():
    try:
        onboard_user(issue)
        return {'status': "Success."}
    except:
        return {'status': "An error ocurred."}


@app.route('/offboard', methods=['POST'])
def index():
    try:
        functions.jira_parser(app.current_request.json_body)
        return {'status': "Not setup."}
    except:
        return {'status': "An error ocurred."}


@app.route('/infochange', methods=['POST'])
def index():
    try:
        return {'status': "Not setup."}
    except:
        return {'status': "An error ocurred."}

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
