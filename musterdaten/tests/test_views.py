from musterdaten.test import TestCase

class TestIndex(TestCase):
    def test_ok(self):
        self.get_check_200("musterdaten:index")

