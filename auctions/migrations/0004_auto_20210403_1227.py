# Generated by Django 2.2.12 on 2021-04-03 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210403_1225'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='user_id',
            new_name='user',
        ),
    ]
