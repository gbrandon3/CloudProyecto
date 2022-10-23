from email.mime.text import MIMEText
import smtplib, ssl
import app_settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MailSend():

    def send_email(self, destination_address, subject, messageBody):
        context = ssl._create_unverified_context()

        server = smtplib.SMTP(app_settings.EMAIL_SERVER,app_settings.EMAIL_SERVER_PORT)
        try:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(app_settings.EMAIL_USER, app_settings.EMAIL_PASSWORD)
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = app_settings.EMAIL_USER
            message["To"] = destination_address
            mailPart = MIMEText(messageBody, "html")
            message.attach(mailPart)
            server.sendmail(app_settings.EMAIL_USER, destination_address, message.as_string())

        except Exception as e:
            print(e)
        finally:
            server.quit() 
