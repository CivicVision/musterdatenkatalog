import csv

from django.core.management import BaseCommand

from musterdaten.management.commands.import_csv_data import get_data
from musterdaten.models import City, Modelsubject, Dataset, Modeldataset, Top3


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--url', dest='url', required=True,
            help='The URL of the CSV file to be imported',
        )

    def handle(self, *args, **options):
        url = options['url']
        lines = get_data(url)
        csv_reader = csv.reader(lines)
        line_count = 0
        errors = 0
        for row in csv_reader:
            if line_count == 0:
                # Header: skip
                line_count += 1
                continue
            else:
                line_count += 1

                try:
                    dataset_title = row[2]
                    city_name = row[3]
                    modelsubject_title, modeldataset_title = row[4].split(" - ")
                    predicted_modelsubject_title, predicted_modeldataset_title = row[5].split(" - ")
                    pred = row[6]

                    modelsubject = Modelsubject.objects.get(
                        title=modelsubject_title)

                    modeldataset = Modeldataset.objects.get(
                        title=modeldataset_title,
                        modelsubject=modelsubject
                    )
                    predicted_modelsubject = Modelsubject.objects.get(
                        title=predicted_modelsubject_title)

                    predicted_modeldataset = Modeldataset.objects.get(
                        title=predicted_modeldataset_title,
                        modelsubject=predicted_modelsubject
                    )
                    city = City.objects.get(name=city_name)
                    dataset = Dataset.objects.filter(
                        title=dataset_title,
                        city=city
                    ).first()

                    Top3.objects.create(
                        dataset=dataset, modeldataset=predicted_modeldataset, pred=pred)
                except Exception as e:
                    print(
                        f"\033[91mImport failed - Dataset: {row[2]} - Modeldataset: {row[5]} [{e}]")
                    errors += 1
                    continue

        line_count = line_count - 1 - errors
        print(f"\033[92mImported {line_count} lines.")
        print(f"\033[91m{errors} errors")
