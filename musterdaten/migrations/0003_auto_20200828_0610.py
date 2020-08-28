# Generated by Django 3.0.8 on 2020-08-28 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('musterdaten', '0002_auto_20200827_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=64),
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='categories',
        ),
        migrations.AddField(
            model_name='dataset',
            name='categories',
            field=models.ManyToManyField(to='musterdaten.Category'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='musterdaten.City'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='description',
            field=models.CharField(max_length=512, verbose_name='beschreibung'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='original_id',
            field=models.CharField(max_length=64, verbose_name='portal_id'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='title',
            field=models.CharField(max_length=64, verbose_name='titel'),
        ),
        migrations.AlterField(
            model_name='leika',
            name='description',
            field=models.CharField(max_length=512),
        ),
    ]
