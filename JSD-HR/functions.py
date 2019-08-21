import smtplib
import ssl
import os
import sys
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
load_dotenv()

def generate_email(template):
    if template == "employee":
        message = """Subject: Hi there

This message is for the employee.

Best,
Snapsheet HR"""
        return message
    elif template == "payroll":
        message = """Subject: Hi there

This is an email.

Best,
Snapsheet HR"""
        return message
    elif template == "manager":
        message = """Subject: Hi there

This message is for the manager."""
        return message
    elif template == "it":
        message = """Subject: Hi there

This message is for IT."""
        return message
    else:
        print("Template failed to generate.")
        sys.exit(1)


def send_email(toaddress, message):
    gmail_user = os.getenv("EMAIL_ACCT")
    gmail_password = os.getenv("EMAIL_PWD")
    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, toaddress, message)


# def jira_parser(request):
#     try:
#     # parse request payload data
#         issue_id = request['issue']['id']
#         issue_key = request['issue']['key']
#     # parse issue fields
#         issue_priority = request['issue']['fields']['priority']['name']
#         issue_creator_username = request['issue']['fields']['creator']['name']
#         issue_creator_displayname = request['issue']['fields']['creator']['displayName']
#         issue_reporter_username = request['issue']['fields']['reporter']['name']
#         issue_reporter_displayname = request['issue']['fields']['reporter']['displayName']
#         issue_type = request['issue']['fields']['issuetype']['name']
#         issue_project = request['issue']['fields']['project']['key']
#         issue_summary = request['issue']['fields']['summary']
#         issue_description = request['issue']['fields']['description']
#     except:
#         return "Error with Jira ticket info."
#
#     jira_dict = {
#         'id': issue_id,
#         'key': issue_key,
#         'priority': issue_priority,
#         'createdby_user': issue_creator_username,
#         'createdby_dispname': issue_creator_displayname,
#         'reporter_user': issue_reporter_username,
#         'reporter_dispname': issue_reporter_displayname,
#         'type': issue_type,
#         'project': issue_project,
#         'summary': issue_summary,
#         'description': issue_description
#     }
#
#     return jira_dict
