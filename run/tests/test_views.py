from django.core.urlresolvers import reverse
from django.test import TestCase

from run.models import AflRun


class RunViewTestCase(TestCase):
    def test_run_view(self):
        url = reverse('run')
        res = self.client.get(url)
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, AflRun.objects.count())
