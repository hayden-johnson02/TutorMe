# Generated by Django 4.1.5 on 2023-03-28 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutorme', '0005_alter_tutorrequest_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutorrequest',
            name='course',
        ),
    ]
