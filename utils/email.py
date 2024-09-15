from django.core.mail import send_mail
from django.conf import settings


def send_email(subject, message, to_mail):
    """
    Sends an email using Django's send_mail function.

    Args:
        subject (str): The subject of the email.
        message (str): The body of the email.
        to_mail (str): The recipient email address.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_mail, ]
        )
        return True
    except Exception as e:
        return False