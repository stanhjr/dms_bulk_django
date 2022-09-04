from django.db import migrations
from order.models import Board


def create_default_board(apps, schema_editor):
    board = Board.objects.create(
        instagram_board_quantity=['4$ per 1k', '3$ per 1k', '2.8$ per 1k', '2.8$ per 1k', '2.5$ per 1k', '2.5$ per 1k',
                                  '2$ per 1k', '2$ per 1k', '2$ per 1k', '1.9$ per 1k', '1.7$ per 1k', '1.7$ per 1k',
                                  '1.7$ per 1k', '1.7$ per 1k', '1.7$ per 1k', '1.7$ per 1k', '1.5$ per 1k'],
        instagram_board_amount=['20000k', '50k', '100k', '150k', '200k', '300k', '400k', '500k', '600k', '700k', '800k',
                                '1m', '1.5m', '2m', '3m', '4m', '5m'],
        instagram_board_discount=['0%', '25%', '30%', '30%', '30%', '38%', '43%', '50%', '50%', '50%', '53%', '57%',
                                  '57%', '57%', '57%', '57%', '63%'],
        instagram_board_total=['80$', '150$', '280$', '420$', '560$', '750$', '920$', '1000$', '1200$', '1400$',
                               '1520$', '1700$', '2550$', '3400$', '5100$', '6800$', '7500$'],

        twitter_board_quantity=['25$ per 1k', '22$ per 1k', '22$ per 1k', '20$ per 1k', '20$ per 1k', '18$ per 1k',
                                '18$ per 1k', '18$ per 1k', '17$ per 1k', '17$ per 1k', '17$ per 1k', '15$ per 1k'],
        twitter_board_amount=['10k', '50k', '75к', '100k', '150к', '200k', '250к', '300k', '500k', '600к', '700k',
                              '1m'],
        twitter_board_discount=['0%', '12%', '12%', '20%', '20%', '28%', '28%', '28%', '32%', '32%', '32%', '40%'],
        twitter_board_total=['250$', '1100$', '1650$', '2000$', '3000$', '3600$', '4500$', '5400$', '8500$', '10200$',
                             '11900$', '15000$'],

        discord_board_quantity=['25$ per 1k', '22$ per 1k', '22$ per 1k', '20$ per 1k', '20$ per 1k', '18$ per 1k',
                                '18$ per 1k', '18$ per 1k', '17$ per 1k', '17$ per 1k', '17$ per 1k', '15$ per 1k'],
        discord_board_amount=['10k', '50k', '75к', '100k', '150к', '200k', '250к', '300k', '500k', '600к', '700k',
                              '1m'],
        discord_board_discount=['0%', '12%', '12%', '20%', '20%', '28%', '28%', '28%', '32%', '32%', '32%', '40%'],
        discord_board_total=['250$', '1100$', '1650$', '2000$', '3000$', '3600$', '4500$', '5400$', '8500$', '10200$',
                             '11900$', '15000$'],

        telegram_board_quantity=['40$ per 1k', '39$ per 1k', '39$ per 1k', '38$ per 1k', '37$ per 1k', '37$ per 1k',
                                 '37$ per 1k', '36$ per 1k', '36$ per 1k', '36$ per 1k', '35$ per 1k'],
        telegram_board_amount=['10k', '20к', '30k', '40k', '50k', '60к', '70k', '100k', '120к', '150k', '300k'],
        telegram_board_discount=['0%', '3%', '3%', '5%', '8%', '8%', '8%', '10%', '10%', '10%', '13%'],
        telegram_board_total=['400$', '780$', '1170$', '1520$', '1850$', '2220$', '2590$', '3600$', '4320$', '5400$',
                              '10500$'],

        )

    board.save()


class Migration(migrations.Migration):
    dependencies = [
        ('order', '0002_board_discord_board_total_and_more'),
    ]
    operations = [
        migrations.RunPython(create_default_board),
    ]
