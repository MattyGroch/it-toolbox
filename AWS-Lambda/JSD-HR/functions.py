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


def generate_email(template, employee):
    if template == "employee":
        message = f"""Subject: Welcome to Snapsheet, {employee.preferredname}!

Hi {employee.preferredname},

We are so happy to have you joining us! Please arrive to the office at 1 N. Dearborn at 9:00am on your start date. Our Office Manager will greet you upon arrival to the 6th floor.


New Hire Paperwork:
You will receive an email from Gina Kraft with a link to PrismHR. Please complete the onboarding documents.

Benefits:
Please complete the benefits enrollment section of the onboarding site. You MUST have this completed by the end of your first week. If you have any questions, feel free to contact us at carly.stieve@snapsheet.me

Forms to bring the first day:
We are required by federal regulations to verify your employment eligibility. Bring supporting documentation for your I-9, in original form. Please refer to the I-9 section of the onboarding site to see a list acceptable documents.


We are excited to have you on the team!

See you soon!"""
        return message
    elif template == "payroll":
        message = """Subject: Hi there

This is an email.

Best,
Snapsheet HR"""
        return message
    elif template == "manager":
        message = f"""Subject: New Hire - {employee.preferredname} {employee.lastname}

Hi There!

Please follow the attached New Hire Checklist as a reminder to set up seating, goals, lunches, etc. in regards to employee name and start date! Also, please provide the following information at your earliest convenience:

    -Where would you like her to sit?
    -Does she need any special equipment from IT?
    -Will she need a cell phone reimbursement? As a reminder, the employee is eligible for a cell phone reimbursement if they are expected to use their personal mobile device for work-related purposes.

Let me know if you have any questions and I look forward to hearing from you!

Best,
Snapsheet HR"""
        return message


def send_email(toaddress, message):
    gmail_user = os.getenv("EMAIL_ACCT")
    gmail_password = os.getenv("EMAIL_PWD")
    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, toaddress, message)


def onboard_user(issue, employee):
    try:
        send_email("matt.grochocinski@snapsheet.me", generate_email("payroll", employee))
        add_jirasd_comment(issue.id, "Cognos email sent.")
    except:
        add_jirasd_comment(issue.id, "Cognos email failed to send. Please send manually.")
    try:
        create_jira_issue("SDESK", employee)
        add_jirasd_comment(issue.id, "IT ticket created.")
    except:
        add_jirasd_comment(issue.id, "Failed to notify IT. Please let IT know manually.")


def change_user(issue, employee):
    try:
        return {'status': "Success."}
    except:
        return {'status': "An error ocurred."}


def terminate_user(issue, employee):
    try:
        return {'status': "Success."}
    except:
        return {'status': "An error ocurred."}


def add_jirasd_comment(issueId, commentBody):
    url = os.getenv("ATLASSIAN_URL") + "/rest/servicedeskapi/request/" + issueId + "/comment"
    auth = "Basic " + os.getenv("JIRA_API_AUTH")
    headers = {
       "Accept": "application/json",
       "Content-Type": "application/json",
       "Authorization": auth
    }
    payload = json.dumps( {
      "public": false,
      "body":  commentBody
    } )
    response = requests.post(
       url,
       data=payload,
       headers=headers
    )

    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))


def create_jira_issue(employee):
    url = os.getenv("ATLASSIAN_URL") + "/rest/servicedeskapi/request"
    auth = "Basic " + os.getenv("JIRA_API_AUTH")
    headers = {
       "Accept": "application/json",
       "Content-Type": "application/json",
       "Authorization": auth
    }
    payload = json.dumps( {
    "serviceDeskId": "3",
    "requestTypeId": "32",
    "requestFieldValues": {
        "summary": f"New Hire: {employee.preferredname} {employee.lastname}",
        "description": f"""
        Title: {employee.title}
        Department: {employee.department}
        Manager: {employee.manager}

        Work Location: {employee.location}
        """
    },
    "requestParticipants": [
        "chris.garzon"
    ]
}
)

    response = requests.post(
       url,
       payload,
       headers
    )


def testissue():
    url = os.getenv("ATLASSIAN_URL") + "/rest/servicedeskapi/request"
    auth = "Basic " + os.getenv("JIRA_API_AUTH")
    headers = {
       "Accept": "application/json",
       "Content-Type": "application/json",
       "Authorization": auth
    }
    payload = json.dumps( {
        "serviceDeskId": "3",
        "requestTypeId": "32",
        "requestFieldValues": {
            "summary": "New Hire: Yaboi Chris",
            "description": "Get him up in herec"
        },
        "requestParticipants": [
            "jose.giron"
        ]
    }
)

    response = requests.post(
           url,
           payload,
           headers
        )

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
