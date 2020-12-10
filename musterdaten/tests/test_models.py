from musterdaten.test import TestCase
from django.db.models import Avg

from musterdaten.tests.factories import (
    DatasetFactory,
    ModeldatasetFactory,
    Top3Factory
)
from musterdaten.models import Top3Modelsubject, Top3Modeldataset, Top3

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

class TestTop3Modelsubject(TestCase):
    def test_title(self):
        top3 = Top3Factory()
        top3_o = Top3.objects.select_related().values(
            'modeldataset__modelsubject__id',
            'modeldataset__modelsubject__title',
        ).annotate(pred=Avg('pred')).order_by('-pred')
        modelsubject = Top3Modelsubject(top3_o[0])

        assert modelsubject.title == top3.modeldataset.modelsubject.title

    def test_pred_percentage(self):
        top3 = Top3Factory(pred=0.4)
        top3_o = Top3.objects.select_related().values(
            'modeldataset__modelsubject__id',
            'modeldataset__modelsubject__title',
        ).annotate(pred=Avg('pred')).order_by('-pred')
        modelsubject = Top3Modelsubject(top3_o[0])

        assert modelsubject.prediction_percentage == 40

    def test_pred_percentage_100(self):
        top3 = Top3Factory(pred=1.4)
        top3_o = Top3.objects.select_related().values(
            'modeldataset__modelsubject__id',
            'modeldataset__modelsubject__title',
        ).annotate(pred=Avg('pred')).order_by('-pred')
        modelsubject = Top3Modelsubject(top3_o[0])

        assert modelsubject.prediction_percentage == 100


class TestTop3Modeldataset(TestCase):
    def test_title(self):
        top3 = Top3Factory()
        top3_o = Top3.objects.select_related().values(
            'modeldataset_id',
            'modeldataset__title',
        ).annotate(pred=Avg('pred')).order_by('-pred')
        modeldataset = Top3Modeldataset(top3_o[0])

        assert modeldataset.title == top3.modeldataset.title

    def test_pred_percentage(self):
        top3 = Top3Factory(pred=0.4)
        top3_o = Top3.objects.select_related().values(
            'modeldataset_id',
            'modeldataset__title',
        ).annotate(pred=Avg('pred')).order_by('-pred')
        modeldataset = Top3Modeldataset(top3_o[0])

        assert modeldataset.prediction_percentage == 40

    def test_pred_percentage_100(self):
        top3 = Top3Factory(pred=1.4)
        top3_o = Top3.objects.select_related().values(
            'modeldataset_id',
            'modeldataset__title',
        ).annotate(pred=Avg('pred')).order_by('-pred')
        modeldataset = Top3Modeldataset(top3_o[0])

        assert modeldataset.prediction_percentage == 100
