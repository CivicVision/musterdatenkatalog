import json
from api.test import APITestCase

from musterdaten.tests.factories import (
    ModeldatasetFactory,
)

class TestModeldataset(APITestCase):
    def test_ok(self):
        self.get('api:modeldataset-list', extra={'format': 'json'})
        self.assert_http_200_ok()

    def test_search_ok(self):
        self.get('api:modeldataset-search', data={ 'q': "test" }, extra={'format': 'json'})
        self.assert_http_200_ok()

    def test_search_result(self):
        dataset = ModeldatasetFactory(title="San Diego")

        response = self.get('api:modeldataset-search', data={ 'q': "ego" }, extra={'format': 'json'})
        data = json.loads(response.content)

        self.assert_http_200_ok()
        assert len(data) == 1
        assert data[0]["title"] == dataset.title
