# Generated by Django 2.1.3 on 2018-12-09 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0008_auto_20181209_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendmessageagain',
            name='time_received',
            field=models.TimeField(auto_now_add=True),
        ),
    ]