# Generated by Django 3.1.5 on 2021-01-06 22:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0002_auto_20210106_1725'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='peep',
            new_name='caption',
        ),
    ]
