import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='titel')),
                ('DCAT_AP', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Kategorie',
                'verbose_name_plural': 'Kategorien',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name': 'Stadt',
                'verbose_name_plural': 'Städte',
            },
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='titel')),
                ('description', models.CharField(max_length=128, verbose_name='beschreibung')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='erstellt_am')),
                ('original_id', models.CharField(max_length=32, verbose_name='portal_id')),
                ('url', models.URLField()),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='geändert_am')),
                ('metadata_created', models.DateTimeField(verbose_name='metadaten_erstellt')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='musterdaten.Category', verbose_name='Kategorie')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='musterdaten.City', verbose_name='Stadt')),
            ],
            options={
                'verbose_name': 'Datensatz',
                'verbose_name_plural': 'Datensätze',
            },
        ),
        migrations.CreateModel(
            name='Leika',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='titel')),
                ('code', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='titel')),
                ('url', models.URLField()),
                ('short_title', models.CharField(max_length=32)),
            ],
            options={
                'verbose_name': 'Lizenz',
                'verbose_name_plural': 'Lizenzen',
            },
        ),
        migrations.CreateModel(
            name='Modeldataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='titel')),
                ('leika', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='musterdaten.Leika')),
            ],
            options={
                'verbose_name': 'Musterdatensatz',
                'verbose_name_plural': 'Musterdatensätze',
            },
        ),
        migrations.CreateModel(
            name='Modelsubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='titel')),
            ],
            options={
                'verbose_name': 'Thema',
                'verbose_name_plural': 'Themen',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': 'Bundesland',
                'verbose_name_plural': 'Bundesländer',
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('session_id', models.CharField(max_length=32)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='musterdaten.Dataset')),
                ('modeldataset', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='musterdaten.Modeldataset')),
            ],
            options={
                'verbose_name': 'Bewertung',
                'verbose_name_plural': 'Bewertungen',
            },
        ),
        migrations.AddField(
            model_name='modeldataset',
            name='modelsubject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='musterdaten.Modelsubject'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='license',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='musterdaten.License'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='modeldataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='musterdaten.Modeldataset'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='top_3',
            field=models.ManyToManyField(related_name='dataset_top3', to='musterdaten.Modeldataset'),
        ),
    ]
