import sys
# import smtplib
import requests
from requests.auth import HTTPBasicAuth 
# from email.message import EmailMessage

class AgoraEmailer:
    def __init__(self, password, host):
        self.password = password
        self.host = host
        self.devs = []

    def setDeveloperEmails(self, emails):
        self.devs = emails.split(',')

    def sendEmail(self, receiver, subject, message):
        auth = HTTPBasicAuth('api', self.password)
        form = {
            "from": f"Agora Gods <postmaster@{self.host}>",
            "to": receiver,
            "subject": subject,
            "text": message
        }
        res = requests.post(f"https://api.mailgun.net/v3/{self.host}/messages", auth=auth, data=form)

    def confirmAccountEmail(self, receiver, url, backup):
        subject = "Confirm your Agora account"
        message = f"Confirm your new Agora account by visiting the following page:\n{url}\nYour account backup recovery code is {backup}. Don't lose it!"
        self.sendEmail(receiver, subject, message)

    def recoverAccountEmail(self, receiver, url):
        subject = "Recover your Agora account"
        message = f"Recover your Agora account by visiting the following page:\n{url}"
        self.sendEmail(receiver, subject, message)

    def newRecoveryToken(self, receiver, recovery):
        subject = "New recovery token"
        message = f"You have recently changed your email or used your former recovery token.\n Here is your new recovery token: {recovery}"
        self.sendEmail(receiver, subject, message)

    def changeAccountEmail(self, receiver, url):
        subject = "Confirm your new Agora email"
        message = f"Confirm that this is your new email for your Agora account by visiting the following page:\n{url}"
        self.sendEmail(receiver, subject, message)

    def deleteAccountEmail(self, receiver, url):
        subject = "Confirm deletion of your Agora account"
        message = f"Visit the following page to confirm the deletion of your Agora account:\n{url}"
        self.sendEmail(receiver, subject, message)

    def bugReport(self, rid, user, content):
        subject = f"Bug report #{rid}"
        message = f"Bug report submitted by user {user}:\n\n{content}"
        for em in self.devs:
            self.sendEmail(em, subject, message)
