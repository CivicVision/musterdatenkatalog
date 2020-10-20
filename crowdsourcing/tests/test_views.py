from musterdaten.test import TestCase

from musterdaten.tests.factories import (
    DatasetFactory,
    ModeldatasetFactory,
)
class TestIndex(TestCase):
    def test_ok(self):
        self.get_check_200("crowdsourcing:index")

class TestEvaluate(TestCase):
    def test_ok(self):
        dataset = DatasetFactory()
        modeldataset = ModeldatasetFactory()
        data = {"dataset": str(dataset.id), "modeldataset": str(modeldataset.id) }

        response = self.post('crowdsourcing:evaluate', data=data)
        self.response_302(response)

    def test_failure(self):
        dataset = DatasetFactory()
        modeldataset = ModeldatasetFactory()
        data = {"dataset": "stri", "modeldataset": str(modeldataset.id) }

        response = self.post('crowdsourcing:evaluate', data=data)
        self.response_400(response)
