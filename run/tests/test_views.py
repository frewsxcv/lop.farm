import os

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from run.models import AflRun, Run
from run.tasks import AFL_OUTPUT_DIR


class RunViewTestCase(TestCase):
    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_run_view(self):
        url = reverse('run')
        res = self.client.get(url)
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, AflRun.objects.count())

        run = Run.objects.get()
        self.assertIsNotNone(run.queued_on)
        self.assertIsNotNone(run.started_on)
        self.assertIsNotNone(run.completed_on)

        self.assertFalse(os.path.exists(AFL_OUTPUT_DIR))
