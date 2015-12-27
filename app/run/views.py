import shutil

from django.http import HttpResponseServerError
from django.shortcuts import render

from run.models import Run
from run.tasks import run_afl, PY_AFL_FUZZ_CMD


def run(request):
    if not shutil.which(PY_AFL_FUZZ_CMD):
        return HttpResponseServerError()

    run = Run.objects.create()
    run_afl.delay(run.id, 10)

    return render(request, 'run.html')
