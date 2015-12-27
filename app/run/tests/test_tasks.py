import os

from django.test import TestCase

from run.models import AflRun, Run
from run.tasks import AFL_OUTPUT_DIR, run_afl


class RunTasksTestCase(TestCase):
    def test_run_afl(self):
        run = Run.objects.create()
        run_afl(run.id, 10)

        self.assertEqual(1, AflRun.objects.count())

        run = Run.objects.get()
        self.assertIsNotNone(run.queued_on)
        self.assertIsNotNone(run.started_on)
        self.assertIsNotNone(run.completed_on)

        self.assertFalse(os.path.exists(AFL_OUTPUT_DIR))
