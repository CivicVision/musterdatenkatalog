from io import StringIO
from django.core.management import call_command
from django.test import TestCase

from musterdaten.models import Dataset, Modeldataset, Modelsubject, License, Category, City

class ImportCSVDataTest(TestCase):
    def test_should_create_all_datasets(self):
        call_command('import_csv_data', url="./musterdaten/tests/fixtures/import_data.csv")
        self.assertTrue(Dataset.objects.all().exists())
        self.assertTrue(Modeldataset.objects.all().exists())
        self.assertTrue(Modelsubject.objects.all().exists())
        self.assertTrue(License.objects.all().exists())
        self.assertTrue(Category.objects.all().exists())
        self.assertTrue(City.objects.all().exists())
        self.assertEqual(len(Category.objects.all()),2)

    def test_does_not_create_any_datasets_for_malformed_data(self):
        call_command('import_csv_data', url="./musterdaten/tests/fixtures/malformed_data.csv")
        self.assertFalse(Dataset.objects.all().exists())
