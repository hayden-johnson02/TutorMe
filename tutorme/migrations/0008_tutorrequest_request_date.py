# Generated by Django 4.1.5 on 2023-03-31 15:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorme', '0007_tutorrequest_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorrequest',
            name='request_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]