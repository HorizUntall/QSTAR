import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

class QSTARemailer:
    def __init__(self):
        self.email_sender = 'qstarlibraryzrc@gmail.com'
        self.email_password = 'owll nqwi cbew jhhq'
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587

    def send_email(self, filepath, send_to=['rbihag@zrc.pshs.edu.ph'], subject="QSTAR Report", body='This is a report from QSTAR'):
        for person in send_to:
            msg = MIMEMultipart()
            msg['From'] = self.email_sender
            msg['To'] = person
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            #open the file in python as a binary
            attachment = open(filepath, 'rb') # r for read and b for binary

            #Encode as base 64
            attachment_package = MIMEBase('application', 'octet-stream')
            attachment_package.set_payload((attachment).read())
            encoders.encode_base64(attachment_package)
            attachment_package.add_header('Content-Disposition', 'attachment; filename='+filepath)
            msg.attach(attachment_package)

            text = msg.as_string()

            try:
                TIE_server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                TIE_server.starttls()
                TIE_server.login(self.email_sender, self.email_password)
                TIE_server.sendmail(self.email_sender, person, text)
            except Exception:
                print("Incorrect email format for sender:", person)


