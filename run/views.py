import shutil

from django.http import HttpResponseServerError
from django.shortcuts import render

from run.tasks import run_afl, PY_AFL_FUZZ_CMD


def run(request):
    if not shutil.which(PY_AFL_FUZZ_CMD):
        return HttpResponseServerError()

    run_afl.delay()

    return render(request, 'run.html')
