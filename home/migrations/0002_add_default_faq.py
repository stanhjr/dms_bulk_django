from django.db import migrations

from home.models import FAQModel


def create_default_faq_questions(*args, **kwargs):
    FAQModel.objects.bulk_create([
        FAQModel(question='How i will know that all messages are send?',
                 answer='Firstly you will see in your dashboard process of campaign and monitor how messages sending in live by progress tab and after messages done you will be able to download screenshot of software.'),
        FAQModel(question='Do you have discounts on big volumes?',
                 answer='If you are ordering from us more then 1-5m DMS in week (depends on social media) we can offer special price with discount code'),
        FAQModel(question='Can my account be blocked after Mass DM?',
                 answer='No, it will not be blocked, we are using our accounts to send messages. We take care about our clients safety'),
        FAQModel(question='How fast leads will come?', answer='Leads is fully depends how you convert traffic and your chosen targets quality, we guarantee that all messages will be send properly: All amount, each message with push notification. So as we cannot control when someone opens their Direct Message in: Instagram, Twitter, Telegram or Discord, we say to expect that main traffic will come in first 24h'),
        FAQModel(
            question='How fast DMs can be sent out in Each of Social Media?', answer='dmsbulk.com guarantees that your order will be done from 24 hours maximum up to 72 hours. Its fully depends on demand and order queue. 72 hours could take only huge bulk orders. More than 1m DMs because of prepare time, but usually order is done much faster'),
    ])


class Migration(migrations.Migration):
    dependencies = [
        ('home', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_default_faq_questions),
    ]
