from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#from email.mime.base import MIMEBase
#from email import encoders
import smtplib
import os
from dotenv import load_dotenv
load_dotenv()

email_user = os.getenv('EMAIL_ID')
email_password = os.getenv('PASSWORD')
email_send = os.getenv('TO')

def mail(subject, body):

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    msg.attach(MIMEText(body,'plain'))

    '''
    filename='some file with spaces'
    attachment  =open(filename,'rb')

    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= "+filename)
    '''


    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email_user,email_password)


    server.sendmail(email_user,email_send,text)
    server.quit()
