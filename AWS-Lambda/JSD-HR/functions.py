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


def build_email(type, e, files=None):
    # Define required variables
    gmail_user = os.getenv("EMAIL_ACCT")
    from_addr = os.getenv("HR_REPLYTO")
    toaddr = {
        "Cognos": os.getenv("HR_SEND_EMAILS"),
        "Manager": e.manager_email,
        "New Hire": e.email,
        "Test": "matt.grochocinski@snapsheet.me"
    }

    subj = {
        "Cognos": f"Snapsheet New Hire - {e.firstname} {e.lastname}",
        "Manager": f"{e.department} New Hire - {e.preferredname} {e.lastname}",
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
        "Manager": f"""Hi {e.manager},

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
Dearborn on {e.start_date} at 10:00 AM. Our Office Manager, Steven Stojak will greet you
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
    msg['From'] = "Snapsheet HR <%s>" % from_addr
    msg['To'] = toaddr[type]
    msg['Subject'] = subj[type]
    msg.attach(MIMEText(body[type], 'plain'))
    # Identify and attach filelist
    if files != None:
        tmp_path = os.getcwd() + "/tmp/"
        for f in files:
            part = MIMEBase('application', "octet-stream")
            part.set_payload( open(tmp_path + f,"rb").read() )
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
            msg.attach(part)
    return msg

def send_email(msg):
    # Define sending variables
    gmail_user = os.getenv("EMAIL_ACCT")
    gmail_password = os.getenv("EMAIL_PWD")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_user, gmail_password)
        server.sendmail(msg['From'], msg['To'].split(","), msg.as_string())
        server.quit()


def add_jirasd_comment(issueKey, commentBody):
    url = "%s/rest/servicedeskapi/request/%s/comment" % (jira_url(), issueKey)
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

    combo = "%s:%s" % (user, key)

    b64 = base64.b64encode(combo.encode()).decode()

    auth = "Basic %s" % b64

    return auth


def jira_url():
    domain = os.getenv("JIRA_DOMAIN")
    url = "https://%s.atlassian.net" % domain
    return url


def create_SDESK_issue(employee):
    url = "%s/rest/servicedeskapi/request" % jira_url()
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
            "description": f"""Title: {employee.title}
Department: {employee.department}
Manager: {employee.manager}""",
            "duedate": f"{employee.start_date}"
        }
    }
)
    print(payload)
    response = requests.post(
       url,
       data=payload,
       headers=headers
    )

    newIssue = json.loads(response.text)['issueKey']

    return newIssue


def download_jira_attachments(issueKey):
    tmp_path = os.getcwd() + "/tmp/"
    baseurl = jira_url()
    # url = baseurl + "/rest/servicedeskapi/request/" + issueKey + "/attachment"
    url = "%s/rest/servicedeskapi/request/%s/attachment" % (baseurl, issueKey)
    auth = jira_auth()
    headers = {
        "Authorization": auth
    }
    filelist = list()
    r = requests.get(url, headers = headers, stream = True)
    c = json.loads(r.content)
    if not c['values']:
        return None
    else:
        for a in c['values']:
            filename = a['filename']
            file_url = a['_links']['content']
            z = requests.get(file_url, headers = headers, stream = True)
            with open(tmp_path + filename, "wb") as f:
                f.write(z.content)
            f.close()
            filelist.append(filename)
    return filelist


def link_jira_issues(parentkey, childkey):
    print("Parent: %s" % parentkey)
    print("Child: %s" % childkey)
    baseurl = jira_url()
    url = "%s/rest/api/3/issueLink" % baseurl
    auth = jira_auth()
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": auth
    }

    payload = json.dumps( {
        "outwardIssue": {"key": parentkey},
        "inwardIssue": {"key": childkey},
        "type": {"name": "Child"}
        } )

    response = requests.post(
        url,
        data = payload,
        headers = headers
    )
    return response


def onboard_user(issue, emp):
    # Get any attachments before proceeding
    attachments = download_jira_attachments(issue.key)

    # Build and send the email to Cognos
    email = build_email("Cognos", emp, attachments)
    try:
        send_email(email)
        add_jirasd_comment(issue.key, "Email sent to Cognos.")
    except:
        add_jirasd_comment(issue.key, "We could not send the email to Cognos. Please alert them manually.")

    # Build and send the email to the employee's manager
    email = build_email("Manager", emp)
    try:
        send_email(email)
        add_jirasd_comment(issue.key, "Email sent to employee's manager: %s." % emp.manager)
    except:
        add_jirasd_comment(issue.key, "We could not send an email to %s" % emp.manager_email)

    # Build and send the email to the new hire
    email = build_email("New Hire", emp)
    try:
        send_email(email)
        add_jirasd_comment(issue.key, "Welcome email sent to new hire.")
    except:
        add_jirasd_comment(issue.key, "We could not send the welcome email to the new hire: %s" % emp.email)

    try:
        sdesk_issue = create_SDESK_issue(emp)
        link_jira_issues(issue.key, sdesk_issue)
        add_jirasd_comment(issue.key, "IT ticket created: %s" % sdesk_issue)
    except:
        add_jirasd_comment(issue.key, "Failed to alert IT.")

    add_jirasd_comment(issue.key, "Automation completed.")


def change_user(issue, emp):
    try:
        return {'status': "Success."}
    except:
        return {'status': "An error ocurred."}


def terminate_user(issue, employee):
    try:
        return {'status': "Success."}
    except:
        return {'status': "An error ocurred."}
