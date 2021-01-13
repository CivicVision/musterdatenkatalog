from constance.test import override_config

from musterdaten.test import TestCase
from django.db.models import Avg

from musterdaten.tests.factories import (
    DatasetFactory,
    ModelsubjectFactory,
    ModeldatasetFactory,
    ScoreFactory,
    Top3Factory,
    CustomUserFactory
)
from musterdaten.models import Top3Modelsubject, Top3Modeldataset, Top3, Score, Dataset

class TestDataset(TestCase):
    def test_factory(self):
        dataset = DatasetFactory()

        assert dataset is not None
        assert dataset.title != ""

    def test_str(self):
        dataset = DatasetFactory()

        assert str(dataset) == dataset.title

    @override_config(SCORED_LESS_THAN=2, SCORED_MORE_THAN=1, SCORED_AVAILABLE=1)
    def test_next_dataset_for_user_return_scored_between(self):
        user = CustomUserFactory()
        dataset = DatasetFactory()
        dataset_2 = DatasetFactory()
        ScoreFactory(dataset=dataset)
        ScoreFactory(dataset=dataset)
        ScoreFactory(dataset=dataset_2)

        next_dataset = Dataset.objects.next_dataset_for_user(user)

        assert next_dataset == dataset_2

    @override_config(SCORED_LESS_THAN=3, SCORED_MORE_THAN=0)
    def test_next_dataset_for_user_return_not_scored_by_user(self):
        user = CustomUserFactory()
        dataset = DatasetFactory()
        dataset_2 = DatasetFactory()
        dataset_3 = DatasetFactory()
        ScoreFactory(dataset=dataset, user=user)
        ScoreFactory(dataset=dataset_2, user=user)

        next_dataset = Dataset.objects.next_dataset_for_user(user)

        assert next_dataset == dataset_3

    @override_config(SCORED_LESS_THAN=3, SCORED_MORE_THAN=0)
    def test_next_dataset_for_user_return_not_scored_by_user_less_than(self):
        user = CustomUserFactory()
        dataset = DatasetFactory()
        dataset_2 = DatasetFactory()
        dataset_3 = DatasetFactory()
        dataset_4 = DatasetFactory()
        ScoreFactory(dataset=dataset, user=user)
        ScoreFactory(dataset=dataset_2, user=user)
        ScoreFactory(dataset=dataset_3, user=user)
        ScoreFactory(dataset=dataset_4)

        next_dataset = Dataset.objects.next_dataset_for_user(user)

        assert next_dataset == dataset_4

    @override_config(SCORED_LESS_THAN=3, SCORED_MORE_THAN=2, SCORED_AVAILABLE=1)
    def test_next_dataset_for_user_global_less(self):
        user = CustomUserFactory()
        dataset = DatasetFactory()
        dataset_2 = DatasetFactory()
        ScoreFactory(dataset=dataset)
        ScoreFactory(dataset=dataset)
        ScoreFactory(dataset=dataset)
        ScoreFactory(dataset=dataset)
        ScoreFactory(dataset=dataset_2)

        next_dataset = Dataset.objects.next_dataset_for_user(user)

        assert next_dataset == dataset_2


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
