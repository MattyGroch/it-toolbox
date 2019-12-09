import smtplib
import ssl
import os
import sys
import requests
import json
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv


load_dotenv()


def send_email(category, e, attachments):
    # Define required variables

    toaddr = {
        "Cognos": os.getenv("HR_SEND_EMAILS"),
        "Manager": e.manager_email,
        "New Hire": e.email,
        "Test": "matt.grochocinski@snapsheet.me,jose.giron@snapsheet.me"
    }

    subj = {
        "Cognos": f"Snapsheet New Hire - {e.firstname} {e.lastname}",
        "Manager": f"{e.department} New Hire - {e.firstname} {e.lastname}",
        "New Hire": f"Hey {e.preferredname}! Welcome to Snapsheet!",
        "Test": f"Test HR Email: {e.preferredname} {e.lastname}"
    }

    body = {
        "Cognos": f"""Hi Ann and Gina,

            Please see the information below as well as the attached offer letter for a new hire:
            a. Full Name: {e.firstname} {e.lastname}
            b. Personal Email: {e.email}
            c. Title: {e.title}
            d. Location: {e.location}
            e. Department: {e.department}
            f. Start Date: {e.start_date}
            g. Pay (salary/hourly): {e.wage_amount} ({e.wage_type})
            h. Exemption Status: {e.flsa}
            Let us know if there is any other information you need!""",
        "Manager": f"""Hello {e.manager},

            To ensure that IT and HR can facilitate your new hire's desk setup, please provide the following information in regards to {e.preferredname} {e.lastname} starting on {e.start_date} at 10am.
            ● Where would you like your New Hire to sit?
            ● Does your New Hire need any special equipment from IT?
            ● Will your New Hire need a corporate card/travel?

            We've attached the New Hire Checklist and 30/60/90 in case you'd like to use the
            templates to set up seating, goals, lunches, etc. Let us know if you have any questions.
            We look forward to your reply soon.

            Best,
            Snapsheet HR Team""",
        "New Hire": f"""Hi {e.preferredname},

            We are so happy to have you join us next week! Please arrive to the office at 1 N.
            Dearborn on May 13th at 10:00 AM . Our Office Manager, Steven Stojak will greet you
            upon arrival to the 6th floor.

            New Hire Paperwork:
            You will receive an email from Gina Kraft with a link to PrismHR. Please complete the
            onboarding documents prior to your first day.

            Benefits:
            Please complete the benefits enrollment section of the onboarding site. You MUST have
            this completed by the end of your first week. If you have any questions, feel free to
            contact me at dominique.oconnor@snapsheet.me

            Forms and Identification to bring the first day:
            We are required by federal regulations to verify your employment eligibility. Bring
            supporting documentation for your I-9, in original form. Please refer to the I-9 section of
            the onboarding site to see a list of acceptable documents.

            We are excited to have you on the team!

            See you soon!""",
        "Test": "This is the body of the email."
    }

    # Build the email message
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr[category]
    msg['Subject'] = subj[category]
    msg.attach(MIMEText(body[category], 'plain'))

    # Identify and attach filelist
    if category == "Cognos":
        if attachments is not None:
            attachments = "File_name_with_extension"
            for a in attachments:
                    open(a, "rb")

    # Define sending variables
    gmail_user = os.getenv("EMAIL_ACCT")
    gmail_password = os.getenv("EMAIL_PWD")
    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, msg['To'].split(","), msg.as_string())


def onboard_user(issue, emp):
    jira_files = download_jira_attachments(issue.key)
    mgr_files =
    send_email("Test", emp, files)
    print("Cognos email sent.")
    add_jirasd_comment(issue.key, "Cognos email sent.")

    create_SDESK_issue(emp)
    print("SDESK ticket made.")
    add_jirasd_comment(issue.key, "IT ticket created.")


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


def add_jirasd_comment(issueKey, commentBody):
    url = jira_url() + "/rest/servicedeskapi/request/" + issueKey + "/comment"
    auth = jira_auth()
    headers = {
       "Accept": "application/json",
       "Content-Type": "application/json",
       "Authorization": auth
    }
    body = json.dumps( {
      "public": "false",
      "body": commentBody
    }
)

    response = requests.post(
       url,
       data=body,
       headers=headers
    )

    return response


def jira_auth():
    user = os.getenv("JIRA_ACCT")
    key = os.getenv("JIRA_API_KEY")
    encode = base64.b64encode(acct + ":" key)
    auth = "Basic " + encode
    return auth


def jira_url():
    domain = os.getenv("JIRA_DOMAIN")
    url = "https://" + domain + ".atlassian.net"
    return url


def create_SDESK_issue(employee):
    url = jira_url() + "/rest/servicedeskapi/request"
    auth = jira_auth()
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
            "description": f"Title: {employee.title}"
        },
        "requestParticipants": [
            "chris.garzon"
        ]
    }
)

    requests.post(
       url,
       data=payload,
       headers=headers
    )
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    return response


def testissue():
    url = jira_url() + "/rest/servicedeskapi/request"
    auth = jira_auth()
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
            "description": "Get him up in here!"
        },
        "requestParticipants": [
            "chris.garzon"
        ]
    }
)

    response = requests.post(
           url,
           data=payload,
           headers=headers
        )


def download_jira_attachments(issueKey):
    url = "https://snapsheettech.atlassian.net/rest/servicedeskapi/request/" + issueKey + "/attachment"
    auth = jira_auth()
    headers = {
       "Authorization": auth
    }
    filelist = list()
    r = requests.get(jiraURL, headers=headers, stream = True)
    c = json.loads(r.content)
    if not c['values']:
    	return None
    else:
       	for a in c['values']:
       		filename = a['filename']
    		file_url = a['_links']['content']
       		z = requests.get(file_url, headers=headers, stream = True)
       		with open(filename, "wb") as f:
    			f.write(z.content)
    		f.close()
            file_list.append(filename)
    return file_list
