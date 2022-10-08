import binascii
import os
import smtplib
import ssl
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery.schedules import crontab
from django.conf import settings
from jinja2 import Template
from celery import Celery

from .config import config


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dms_bulk_django.settings")
app = Celery(
    "celery_tasks",
    broker="redis://localhost:6379",
)

app.config_from_object(config)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=23, minute=0),
        update_analytics.s(),
    )


def generate_key() -> str:
    """
    Generated and returned random code

    :return: str: key
    """
    return binascii.hexlify(os.urandom(20)).decode()


@app.task
def send_welcome_to_dmsbulk_message_after_success_verifing(email_to: str) -> str:
    '''
    :param email_to: sender email
    :return: task result
    '''
    password = settings.EMAIL_HOST_PASSWORD
    sender_email = settings.EMAIL_HOST_USER

    receiver_email = email_to
    with open('celery_tasks/templates/02_Mail-Confirmed.html', 'r') as html:
        mail_confirmed_successfully_template = Template(html.read())
    text = mail_confirmed_successfully_template.render()
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = email_to

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "html")
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
def send_verify_link_to_email(username: str, code: str, email_to: str) -> str:
    """
    Sends an email with a link to verify user account

    :param username: DMSbulk username
    :param code: code registration
    :param email_to: sender email
    :return: task result
    """
    password = settings.EMAIL_HOST_PASSWORD
    sender_email = settings.EMAIL_HOST_USER

    receiver_email = email_to
    with open('celery_tasks/templates/01_Verify-Email.html', 'r') as html:
        verify_email_template = Template(html.read())

    text = verify_email_template.render(
        verify_email_link=f"{settings.CELERY_SEND_MAIL_HOST}account/account-activate/?code={code}",
        username=username)
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = email_to
    part1 = MIMEText(text, "html")
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
def send_reset_password_link_to_email(username: str, code: str, email_to: str) -> str:
    """
    Sends an email with a reset password link for user account

    :param code: code registration
    :param email_to: sender email
    :return: task result
    """
    password = settings.EMAIL_HOST_PASSWORD
    sender_email = settings.EMAIL_HOST_USER

    receiver_email = email_to
    with open('celery_tasks/templates/08_Reset-Password.html', 'r') as html:
        reset_password_template = Template(html.read())
    text = reset_password_template.render(
        reset_password_link=f'{settings.CELERY_SEND_MAIL_HOST}account/restore-password/?code={code}',
        username=username)

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = email_to

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "html")
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


@app.task
def update_analytics():
    try:
        from analytics.models import UserStatistics
        from analytics.tools import get_unique_users_today
        number_users_today = get_unique_users_today()
        today = date.today()
        user_statistics = UserStatistics.objects.filter(created_at=today).first()
        if user_statistics:
            user_statistics.visitors_number = number_users_today
        else:
            user_statistics = UserStatistics.objects.create(visitors_number=number_users_today, created_at=today)
        user_statistics.save()
        return f'analytics update, number of users today = {number_users_today}'
    except Exception as e:
        print(e)
