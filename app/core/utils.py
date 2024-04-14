from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings


class Util:
    """A class containing functions to send mails."""

    @staticmethod
    def send_email(data):
        """Send emails with no attachment"""
        email = EmailMessage(subject=data["email_subject"], body=data["email_body"], to=[data["to_email"]])
        email.send()

    @staticmethod
    def send_email_attach(msg, url):
        """Send emails with attachments"""
        body_html = "<html><p>This is your ticket</p></html>"

        message = EmailMultiAlternatives(
            subject=msg["subject"],
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[msg["recipient"]],
        )
        message.mixed_subtype = "related"
        message.attach_alternative(body_html, "text/html")
        message.attach_file("{}".format(url))

        message.send(fail_silently=False)
