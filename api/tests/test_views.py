import factory
from api.test import APITestCase

from musterdaten.tests.factories import (
    ModeldatasetFactory,
    ModelsubjectFactory
)

class TestModeldataset(APITestCase):
    def test_ok(self):
        self.get('api:modeldataset-list', extra={'format': 'json'})

        self.assert_http_200_ok()

    def test_can_retrieve_by_id(self):
        modeldataset = ModeldatasetFactory()

        response = self.get("api:modeldataset-detail", pk=modeldataset.pk)

        self.assert_http_200_ok()
        assert response.data.get("id") == modeldataset.pk

    def test_has_modelsubject_title(self):
        modelsubject = factory.SubFactory(ModelsubjectFactory, title="Whatever")
        modeldataset = ModeldatasetFactory(modelsubject=modelsubject)

        response = self.get("api:modeldataset-detail", pk=modeldataset.pk)

        assert response.data.get("modelsubject").get("title") == "Whatever"

    def test_search_ok(self):
        self.get('api:modeldataset-search', data={ 'q': "test" }, extra={'format': 'json'})

        self.assert_http_200_ok()

    def test_search_result(self):
        dataset = ModeldatasetFactory(title="San Diego")

        response = self.get('api:modeldataset-search', data={ 'q': "ego" }, extra={'format': 'json'})

        self.assert_http_200_ok()
        assert len(response.data) == 1
        assert response.data[0]["title"] == dataset.title
