import re
import threading
from rest_framework.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

email_regex = r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+"
username_regex = r"^[a-z0-9_-]{3,15}$"


def check_login_type(user_input):

    if re.fullmatch(email_regex, user_input):
        return "email"
    elif re.fullmatch(username_regex, user_input):
        return "username"
    else:
        raise ValidationError({"input": "bunaqa kiritip bo'maydi dappa togri kirit"})


class EmailThread(threading.Thread):

    def __init__(self, email):
        super().__init__()
        self.email = email

    def run(self):
        return self.email.send()


def send_email(to_email, code):
    html_content = render_to_string("email/authenticated/index.html", {"code": code})

    email = EmailMessage(subject="Tastiqlaash Kodi", body=html_content, to=[to_email])

    email.content_subtype = "html"

    EmailThread(email).start()
