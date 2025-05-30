import smtplib
from email.mime.text import MIMEText
from backend.core.config import MAIL, PASSWORD, RESET

class EmailService:
    def send_email(self, to: str, subject: str, body: str):
        raise NotImplementedError

class GmailService(EmailService):
    def __init__(self):
        self.mail = MAIL
        self.password = PASSWORD

    def send_email(self, to: str, subject: str, body: str):
        msg = MIMEText(body, "plain")
        msg["From"] = self.mail
        msg["To"] = to
        msg["Subject"] = subject

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(self.mail, self.password)
        server.send_message(msg)
        server.quit()

def build_confirmation_body(token: str) -> str:
    link = f"{RESET}/confirm-email?token={token}"
    return f""" 
Welcome to Behemoth 👾

Please confirm your email by clicking the link below:
{link}

It will expire in 2 days.
"""

def send_password_reset_link(to_email: str, token: str, email_service: EmailService):
    link = f"{RESET}/reset-password?token={token}"
    body = f"""
Your requested reset your Behemoth password.
To continue, click the link below (if your didn't, please ignore this message):

{link}
"""
    email_service.send_email(to_email, "Behemoth recover password.", body)

def send_confirmation_mail(to_email: str, token: str, email_service: EmailService):
    body = build_confirmation_body(token)
    email_service.send_email(to_email, "Behemoth confirmation account.", body)
