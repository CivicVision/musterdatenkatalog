from musterdaten.test import TestCase

from musterdaten.tests.factories import (
    DatasetFactory,
    ModeldatasetFactory,
)
class TestDataset(TestCase):
    def test_factory(self):
        dataset = DatasetFactory()

        assert dataset is not None
        assert dataset.title != ""

    def test_str(self):
        dataset = DatasetFactory()

        assert str(dataset) == dataset.title

class TestModeldataset(TestCase):
    def test_factory(self):
        modeldataset = ModeldatasetFactory()

        assert modeldataset is not None
        assert modeldataset.title != ""

    def test_str(self):
        modeldataset = ModeldatasetFactory()

        assert str(modeldataset) == "{} - {}".format(modeldataset.modelsubject.title, modeldataset.title)

