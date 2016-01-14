import shutil

from django.http import HttpResponseServerError
from django.shortcuts import render

from run.models import Run
from run.tasks import run_afl, PY_AFL_FUZZ_CMD


def trigger_run(request):
    if not shutil.which(PY_AFL_FUZZ_CMD):
        return HttpResponseServerError()

    run = Run.objects.create()
    run_afl.delay(run.id, 10)

    return render(request, 'trigger_run.html')


def run(request, run_id):
    try:
        run = Run.objects.get(id=run_id)
    except Run.DoesNotExist:
        pass

    return render(request, 'run.html', {'run': run})
