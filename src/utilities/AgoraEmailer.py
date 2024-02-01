import sys
import smtplib
from email.message import EmailMessage

class AgoraEmailer:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def auth(self):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(self.username, self.password)
        return server

    def send_email(self, receiver, subject, message):
        message = f"From: {self.username}\nTo: {receiver}\nSubject: {subject}\n\n{message}"
        server = self.auth()
        server.sendmail(self.username, receiver, message)
        server.close()

# send_email(username, password, "franklin@dyer.me", "Hello from python", "Hey bish")
agEm = AgoraEmailer(sys.argv[1], sys.argv[2])
agEm.send_email("franklin@dyer.me", "Hey", "I'm here to kick ass and chew gum. And I'm all out of gum.")
