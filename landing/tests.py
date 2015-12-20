from django.core.urlresolvers import reverse
from django.test import Client, TestCase


class LandingViewTestCase(TestCase):
    def test_landing(self):
        url = reverse('landing')
        res = self.client.get(url)
        self.assertEqual(200, res.status_code)


class LandingTestCase(TestCase):
    def test_no_catch_all(self):
        """Ensure there are no URL routes that catch-all"""
        client = Client()
        response = client.get('/this-should-not-be-a-valid-endpoint')
        self.assertEqual(response.status_code, 404)
