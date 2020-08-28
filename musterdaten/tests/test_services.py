from django.utils import timezone
from test_plus import TestCase

from musterdaten import services
from musterdaten.models import Dataset, Modeldataset, Modelsubject, License, Category, City


class TestAPIDataset(TestCase):
    data = {
        "dataset_title": "Dataset",
        "dataset_description": "DatasetDescription",
        "dataset_original_id": 12345,
        "dataset_metadata_updated_at": timezone.now(),
        "dataset_metadata_generated_at": timezone.now(),
        "dataset_url": "http://www.google.com",
        "modelsubject_title": "ModelsubjectTitle",
        "modeldataset_title": "ModeldatasetTitle",
        "license_title": "License",
        "categories_titles": ["one", "two", "three"],
        "city_name": "Munich"
    }

    def test_create_all_models_with_no_data(self):
        self.assertIsNone(services.create_all_models({}))

    def test_create_all_models_with_valid_data_returns_a_dataset_instance(self):
        dataset = services.create_all_models(self.data)
        self.assertIsInstance(dataset, Dataset)

    def test_create_all_models_with_valid_data(self):
        services.create_all_models(self.data)

        self.assertTrue(Dataset.objects.all().exists())
        self.assertTrue(Modeldataset.objects.all().exists())
        self.assertTrue(Modelsubject.objects.all().exists())
        self.assertTrue(License.objects.all().exists())
        self.assertTrue(Category.objects.all().exists())
        self.assertTrue(City.objects.all().exists())
