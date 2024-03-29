import factory

from api.test import APITestCase
from rest_framework.authtoken.models import Token

from musterdaten.tests.factories import (
    ModeldatasetFactory,
    ModelsubjectFactory,
    ScoreFactory,
    DatasetFactory
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

    def test_cannot_create(self):
        self.post('api:modeldataset-list', data={})

        self.assert_http_405_method_not_allowed()

class TestModelsubject(APITestCase):
    def test_ok(self):
        self.get('api:modelsubject-list', extra={'format': 'json'})

        self.assert_http_200_ok()

    def test_can_retrieve_by_id(self):
        modelsubject = ModelsubjectFactory()

        response = self.get("api:modelsubject-detail", pk=modelsubject.pk)

        self.assert_http_200_ok()
        assert response.data.get("id") == modelsubject.pk

    def test_cannot_create_modelsubject(self):
        self.post('api:modelsubject-list', data={'title': 'Test'})

        self.assert_http_405_method_not_allowed()

class TestScore(APITestCase):
    def test_ok(self):
        self.get('api:score-list', extra={'format': 'json'})

        self.assert_http_200_ok()

    def test_can_retrieve_by_id(self):
        score = ScoreFactory()

        response = self.get("api:score-detail", pk=score.pk)

        self.assert_http_200_ok()
        assert response.data.get("id") == score.pk

class TestDataset(APITestCase):

    def test_ok(self):
        self.get('api:dataset-list', extra={'format': 'json'})

        self.assert_http_200_ok()

    def test_can_retrieve_by_id(self):
        dataset = DatasetFactory()

        response = self.get("api:dataset-detail", pk=dataset.pk)

        self.assert_http_200_ok()
        assert response.data.get("id") == dataset.pk

    def test_has_the_city_name(self):
        dataset = DatasetFactory()

        response = self.get("api:dataset-detail", pk=dataset.pk)

        self.assert_http_200_ok()
        assert response.data.get("city") == "San Diego"

    def test_has_the_license_title(self):
        dataset = DatasetFactory()

        response = self.get("api:dataset-detail", pk=dataset.pk)

        self.assert_http_200_ok()
        assert response.data.get("license") == "Lizenz"

    def test_cannot_create_dataset(self):
        dataset_data = {
            }
        self.post('api:dataset-list', data=dataset_data)

        self.assert_http_401_unauthorized()

    def test_can_create_dataset_when_token_is_valid(self):
        admin = self.make_user(username="admin")
        token, success = Token.objects.get_or_create(user=admin)
        dataset_data = {
            "title": "Dataset",
            "description": "DatasetDescription",
            "original_id": 12345,
            "url": "http://www.google.com",
            "modelsubject": "ModelsubjectTitle",
            "modeldataset": "ModeldatasetTitle",
            "license": "License",
            "categories": ["one", "two", "three"],
            "city": "Munich"

            }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.post('api:dataset-list', data=dataset_data)

        self.assert_http_201_created()

        self.client.credentials()

