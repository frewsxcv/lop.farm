from django.test import Client, TestCase


class LandingTestCase(TestCase):
    def test_no_catch_all(self):
        """Ensure there are no URL routes that catch-all"""
        client = Client()
        response = client.get('/this-should-not-be-a-valid-endpoint')
        self.assertEqual(response.status_code, 404)
