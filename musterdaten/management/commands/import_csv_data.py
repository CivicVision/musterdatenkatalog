import csv
import datetime
from urllib import request

from django.core.management import BaseCommand
from django.utils import timezone
from django.utils.timezone import make_aware
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from musterdaten import services
from musterdaten.models import City, License, Category, Modelsubject, Dataset, Modeldataset

def get_data(url):
    val = URLValidator()
    try:
        val(url)
        response = request.urlopen(url)
        lines = [line.decode('utf-8') for line in response.readlines()]
    except ValidationError:
        response = open(url, 'r')
        lines = response.readlines()
    return lines

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
                try:
                    line_count += 1

                    data = {}
                    data["dataset_title"] = row[0]
                    data["dataset_description"] = row[4]
                    data["dataset_original_id"] = row[5]
                    if row[8] == "":
                        data["dataset_metadata_updated_at"] = timezone.now()
                    else:
                        data["dataset_metadata_updated_at"] = make_aware(
                                datetime.datetime.strptime(row[8], '%Y-%m-%dT%H:%M:%S.%f')
                                )
                    data["dataset_metadata_generated_at"] = timezone.now()
                    data["dataset_url"] = row[10]

                    data["modelsubject_title"] = row[2]
                    data["modeldataset_title"] = row[3]
                    data["license_title"] = row[6]
                    data["categories_titles"] = row[7].split(",")
                    data["city_name"] = row[9]

                    services.create_all_models(data)

                except Exception as e:
                    print(f"\033[91mImport failed - Dataset: {row[0]} - Modeldataset: {row[3]} [{e}]")
                    errors += 1
                    line_count -= 1
                    continue

        line_count -= 1  # do not count the header line
        print(f"\033[92mImported {line_count} lines.")
        print(f"\033[91m{errors} errors")
