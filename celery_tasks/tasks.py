import binascii
import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.utils import timezone
from django.conf import settings
from celery import Celery

from .config import config


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dms_bulk_django.settings")
app = Celery(
    "celery_tasks",
    broker="redis://localhost:6379",
)

app.config_from_object(config)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


def generate_key() -> str:
    """
    Generated and returned random code

    :return: str: key
    """
    return binascii.hexlify(os.urandom(20)).decode()


@app.task
def send_verify_link_to_email(code: str, email_to: str) -> str:
    """
    Sends an email with a link to verify user account

    :param code: code registration
    :param email_to: sender email
    :return: task result
    """
    password = settings.EMAIL_HOST_PASSWORD
    sender_email = settings.EMAIL_HOST_USER

    receiver_email = email_to
    text = f"""\
    Hi,
    How are you?
    This is your registration link:
    {settings.CELERY_SEND_MAIL_HOST}account/account-activate/?code={code}"""

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = email_to
    part1 = MIMEText(text, "plain")
    message.attach(part1)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(settings.EMAIL_HOST, 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

        return "Email sent successfully!"
    except Exception as ex:
        return f"Something went wrong…. {ex}"


@app.task
def send_reset_password_link_to_email(code: str, email_to: str) -> str:
    """
    Sends an email with a reset password link for user account

    :param code: code registration
    :param email_to: sender email
    :return: task result
    """
    password = settings.EMAIL_HOST_PASSWORD
    sender_email = settings.EMAIL_HOST_USER

    receiver_email = email_to
    text = f"""\
    Hi,
    How are you?
    This is your restore password link:
    {settings.CELERY_SEND_MAIL_HOST}account/restore-password/?code={code}"""

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = email_to

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    # part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    # message.attach(part2)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(settings.EMAIL_HOST, 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

        return "Email sent successfully!"
    except Exception as ex:
        return f"Something went wrong…. {ex}"


@app.task
def delete_order_from_actives(order_pk: int) -> str:
    from order.models import OrderModel
    OrderModel.objects.filter(pk=order_pk).update(completed=True)
    return f'Order<{order_pk}> deleted from actives'
