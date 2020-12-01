from musterdaten.test import TestCase

from musterdaten.tests.factories import (
    DatasetFactory,
    ModelsubjectFactory,
    ModeldatasetFactory,
    Top3Factory
)
class TestDataset(TestCase):
    def test_factory(self):
        dataset = DatasetFactory()

        assert dataset is not None
        assert dataset.title != ""

    def test_str(self):
        dataset = DatasetFactory()

        assert str(dataset) == dataset.title

    def test_top3_modelsubjects(self):
        modelsubject = ModelsubjectFactory(title="Test")
        modelsubject_2 = ModelsubjectFactory()
        modeldataset = ModeldatasetFactory(modelsubject=modelsubject)
        modeldataset_2 = ModeldatasetFactory(modelsubject=modelsubject)
        modeldataset_3 = ModeldatasetFactory(modelsubject=modelsubject_2)
        dataset = DatasetFactory(modeldataset=modeldataset)
        top3 = Top3Factory(dataset=dataset, modeldataset=modeldataset, pred=0.6)
        top3_2 = Top3Factory(dataset=dataset, modeldataset=modeldataset_2, pred=0.2)
        top3_3 = Top3Factory(dataset=dataset, modeldataset=modeldataset_3, pred=0.2)

        top3_modelsubjects = dataset.top3_modelsubjects

        assert len(top3_modelsubjects) == 2
        assert sum(c.get('pred') for c in top3_modelsubjects) == 1.0
        assert top3_modelsubjects[0].get('modeldataset__modelsubject__title') == modelsubject.title
        assert top3_modelsubjects[0].get('pred') == 0.8


class TestModeldataset(TestCase):
    def test_factory(self):
        modeldataset = ModeldatasetFactory()

        assert modeldataset is not None
        assert modeldataset.title != ""

    def test_str(self):
        modeldataset = ModeldatasetFactory()

        assert str(modeldataset) == "{} - {}".format(modeldataset.modelsubject.title, modeldataset.title)

