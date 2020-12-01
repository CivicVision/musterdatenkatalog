from musterdaten.test import TestCase

from musterdaten.tests.factories import (
    DatasetFactory,
    ModeldatasetFactory,
)
class TestIndex(TestCase):
    def test_ok(self):
        self.get_check_200("crowdsourcing:index")

