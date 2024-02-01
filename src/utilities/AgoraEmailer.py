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

    def confirm_account_email(self, receiver, url):
        subject = "Confirm your Agora account"
        message = f"Confirm your new Agora account by visiting the following page:\n{url}"
        self.send_email(receiver, subject, message)

    def recover_account_email(self, receiver, url):
        subject = "Recover your Agora account"
        message = f"Recover your Agora account by visiting the following page:\n{url}"
        self.send_email(receiver, subject, message)

    def change_account_email(self, receiver, url):
        subject = "Confirm your new Agora email"
        message = f"Confirm that this is your new email for your Agora account by visiting the following page:\n{url}"
        self.send_email(receiver, subject, message)

    def delete_account_email(self, receiver, url):
        subject = "Confirm deletion of your Agora account"
        message = f"Visit the following page to confirm the deletion of your Agora account:\n{url}"
        self.send_email(receiver, subject, message)

