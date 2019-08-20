import smtplib
import ssl
import os
import sys
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv()

def format_email(template):
    if template == "employee":
        message = """Subject: Hi there

This message is for the employee."""
        return message
    elif template == "payroll":
        message = """Subject: Hi there

This message is for Cognos."""
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
    gmail_user = os.getenv("EMAIL")
    gmail_password = os.getenv("PASS")
    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, toaddress, message)


send_email("matt.grochocinski@snapsheet.me",format_email("tacocat"))
