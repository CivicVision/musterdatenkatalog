# Generated by Django 3.0.8 on 2020-08-27 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('musterdaten', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='metadata_created',
        ),
        migrations.AddField(
            model_name='dataset',
            name='metadata_generated_at',
            field=models.DateTimeField(null=True, verbose_name='metadaten_generiert'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='metadata_updated_at',
            field=models.DateTimeField(null=True, verbose_name='metadaten_geändert_am'),
        ),
        migrations.RenameField(
            model_name='dataset',
            old_name='category',
            new_name='categories',
        ),
        migrations.AlterField(
            model_name='modeldataset',
            name='leika',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='musterdaten.Leika'),
        ),
    ]
