import os

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from run.models import AflRun
from run.tasks import AFL_OUTPUT_DIR


class RunViewTestCase(TestCase):
    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_run_view(self):
        url = reverse('run')
        res = self.client.get(url)
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, AflRun.objects.count())
        self.assertFalse(os.path.exists(AFL_OUTPUT_DIR))
