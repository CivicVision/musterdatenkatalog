from api.test import APITestCase

class TestModeldataset(APITestCase):
    def test_ok(self):
        self.get('api:modeldataset-list', extra={'format': 'json'})
        self.assert_http_200_ok()
    def test_search_ok(self):
        self.get('api:modeldataset-search', { 'q': "test" }, extra={'format': 'json'})
        self.assert_http_200_ok()
