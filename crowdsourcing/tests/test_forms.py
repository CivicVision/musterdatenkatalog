from musterdaten.test import TestCase

from crowdsourcing.forms import ScoreForm

from musterdaten.tests.factories import (
    DatasetFactory,
    ModeldatasetFactory,
)
class TestScoreForm(TestCase):
    def test_invalid_dataset(self):
        """An invalid dataset is a validation error."""
        modeldataset = ModeldatasetFactory()
        data = {"dataset": "nope", "modeldataset": str(modeldataset.id) }
        form = ScoreForm(data=data)

        is_valid = form.is_valid()

        assert not is_valid
        assert "Invalid dataset." in form.non_field_errors()

    def test_invalid_modeldataset(self):
        """An invalid modeldataset is a validation error."""
        dataset = DatasetFactory()
        data = {"dataset": str(dataset.id), "modeldataset": "not really" }
        form = ScoreForm(data=data)

        is_valid = form.is_valid()

        assert not is_valid
        assert "Invalid modeldataset." in form.non_field_errors()

