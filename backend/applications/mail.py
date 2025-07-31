import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from jinja2 import Template
# SMTP Configuration — replace for production use
SMTP_SERVER_HOST = "localhost"         # e.g., "smtp.gmail.com"
SMTP_SERVER_PORT = 1025                # Use 587 or 465 for real email
SENDER_ADDRESS = "vehicleparking@donotreply.in"
SENDER_PASSWORD = ""                   # Empty for localhost/debug SMTP

def send_email(to_address, subject, message, content="plain", attachment_file=None):

    msg = MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = to_address
    msg['Subject'] = subject

    # Attach the message body
    if content == "html":
        msg.attach(MIMEText(message, "html"))
    else:
        msg.attach(MIMEText(message, "plain"))

    # Attach file if provided
    if attachment_file:
        with open(attachment_file, 'rb') as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(attachment_file)}"
            )
        msg.attach(part)

    # Send the email
    try:
        s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
        s.login(SENDER_ADDRESS, SENDER_PASSWORD)  # Uncomment for real servers
        s.send_message(msg)
        s.quit()
        print(f"[MAIL] Email sent to {to_address}")
        return True
    except Exception as e:
        print(f"[MAIL ERROR] Failed to send email to {to_address}: {e}")
        return False
