import csv

from urllib import request

from django.core.management import BaseCommand

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from musterdaten import services


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
                help='The URL of the CSV file to be updated',
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
                    data = services.read_row(row)
                    services.update_models(data)

                except Exception as e:
                    print(f"\033[91mImport failed - Dataset: {row[0]} - Modeldataset: {row[3]} [{e}]")
                    errors += 1
                    line_count -= 1
                    continue

        line_count -= 1  # do not count the header line
        print(f"\033[92mImported {line_count} lines.")
        print(f"\033[91m{errors} errors")
