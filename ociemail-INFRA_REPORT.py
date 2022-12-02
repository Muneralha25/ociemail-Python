# python script for sending SMTP configuration with Oracle Cloud Infrastructure Email Delivery


import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
import os
import email.utils
from email.message import EmailMessage
import ssl
import time

# Replace sender@example.com with your "From" address.
# This address must be verified.
# this is the approved sender email
SENDER = '<email_sender_customer>'
SENDERNAME = 'OCVS-INFRA-REPORT Daily'
 
# Replace recipient@example.com with a "To" address. If your account
# is still in the sandbox, this address must be verified.
RECIPIENT = '<email_customer_received>'
 
# Replace the USERNAME_SMTP value with your Email Delivery SMTP username.
USERNAME_SMTP = 'ocid1.user.oc1..<get OCID> User'


# If you’re using Email Delivery in a different region, replace the HOST value with an appropriate SMTP endpoint.
# Use port 25 or 587 to connect to the SMTP endpoint.
HOST = "smtp.us-ashburn-1.oraclecloud.com"    
PORT = 587
 
# The subject line of the email.
SUBJECT = 'OCVS-INFRA-REPORT Daily'
 
# The email body for recipients with non-HTML email clients.
BODY_TEXT = (
             "This email is sent by the batch command PY INFRA-REPORT Daily. Please check the attachment and validate Health infra OCVS"
            )
 
# get the password from a named config file ociemail.config
#with open(PASSWORD_SMTP_FILE) as f:
#password_smtp = f.readline().strip()

password_smtp = 'null'


dateToday = time.strftime('%Y%m%d')

Path_File = "<windowspath>\OCVS-INFRA-REPORT_"+dateToday+".html"

"""
Path_File = "<<windowspath>\OCVS-INFRA-REPORT_"+dateToday+".html>"
attchment = open(Path_File ,'rb')

att = MIMEBase('application', 'octet-stream')
att.set_payload(attchment.read())
encoders.encode_base64(att)


att.add_header('Content-Disposition', f'attchment; filename=OCVS-INFRA-REPORT_20221107.html')
attchment.close()
"""

with open(Path_File, 'rb') as fp:
	pdf_data = fp.read()
	ctype = 'application/octet-stream'
	maintype, subtype = ctype.split('/', 1)
	


# create message container
msg = EmailMessage()
msg['Subject'] = SUBJECT
msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
msg['To'] = RECIPIENT
msg.set_content(BODY_TEXT)
msg.add_attachment(pdf_data, maintype=maintype, subtype=subtype, filename="OCVS-INFRA-REPORT_"+dateToday+".html")
#msg.add_attachment(att)


# make the message multi-part alternative, making the content the first part
#msg.add_alternative(BODY_TEXT, subtype='text')

# Try to send the message.
try: 
    server = smtplib.SMTP(HOST, PORT)
    server.ehlo()
    # most python runtimes default to a set of trusted public CAs that will include the CA used by OCI Email Delivery.
    # However, on platforms lacking that default (or with an outdated set of CAs), customers may need to provide a capath that includes our public CA.
    server.starttls(context=ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=None, capath=None))
    # smtplib docs recommend calling ehlo() before & after starttls()
    server.ehlo()
    server.login(USERNAME_SMTP, password_smtp)
    # our requirement is that SENDER is the same as From address set previously
    server.sendmail(SENDER, RECIPIENT, msg.as_string())
    server.close()
# Display an error message if something goes wrong.
except Exception as e:
    print(f"Error: {e}")
else:
    print("Email successfully sent!")
