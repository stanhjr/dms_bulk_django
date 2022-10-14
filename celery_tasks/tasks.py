import binascii
import os
import smtplib
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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


def generate_key() -> str:
    """
    Generated and returned random code

    :return: str: key
    """
    return binascii.hexlify(os.urandom(20)).decode()


@app.task
def send_html_email(receiver_email: str, path_to_template: str, subject: str, **kwargs) -> str:
    password = settings.EMAIL_HOST_PASSWORD
    sender_email = settings.EMAIL_HOST_USER
    with open(os.path.join(settings.BASE_DIR, path_to_template), 'r') as html:
        template = Template(html.read())
    email_text = MIMEText(template.render(**kwargs), 'html')

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    message.attach(email_text)

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
    order = OrderModel.objects.get(pk=order_pk)
    order.completed = True
    send_html_email.delay(
        order.order_calc.user.email,
        'celery_tasks/templates/07_Completed.html',
        subject="Order Completed",
        celery_host=settings.CELERY_SEND_MAIL_HOST
    )
    return f'Order<{order_pk}> deleted from actives'


# @app.task
# def update_analytics():
#     try:
#         from analytics.models import UserStatistics
#         from analytics.tools import get_unique_users_today
#         number_users_today = get_unique_users_today()
#         today = date.today()
#         user_statistics = UserStatistics.objects.filter(created_at=today).first()
#         if user_statistics:
#             user_statistics.visitors_number = number_users_today
#         else:
#             user_statistics = UserStatistics.objects.create(visitors_number=number_users_today, created_at=today)
#         user_statistics.save()
#         return f'analytics update, number of users today = {number_users_today}'
#     except Exception as e:
#         print(e)


@app.task
def send_balance_update(email_to: str, cents: int) -> str:
    '''
    :param email_to: sender email
    :return: task result
    '''
    password = settings.EMAIL_HOST_PASSWORD
    sender_email = settings.EMAIL_HOST_USER

    receiver_email = email_to
    with open('celery_tasks/templates/03_Balance.html', 'r') as html:
        mail_confirmed_successfully_template = Template(html.read())
    text = mail_confirmed_successfully_template.render(dasboard_link=f"{settings.CELERY_SEND_MAIL_HOST}dashboard/",
                                                       dollars=cents / 100)
    message = MIMEMultipart("alternative")
    message["Subject"] = "Balance Updated!"
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
