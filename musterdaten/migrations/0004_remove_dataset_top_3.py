# Generated by Django 3.0.8 on 2020-10-20 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musterdaten', '0003_auto_20201020_1007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='top_3',
        ),
    ]
