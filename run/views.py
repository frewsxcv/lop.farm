import os
import shutil
import subprocess

from django.http import HttpResponseServerError
from django.shortcuts import render

from run.afl_utils import stats


PY_AFL_FUZZ_CMD = 'py-afl-fuzz'


def run(request):
    if not shutil.which(PY_AFL_FUZZ_CMD):
        return HttpResponseServerError()

    with open(os.devnull, 'w') as null:
        try:
            subprocess.run([
                PY_AFL_FUZZ_CMD, '-i', '.', '-o', '/tmp/tmpdir', 'python',
                'run/fuzz_cryptography.py'],
                timeout=10,
                stdout=null,
                stderr=null)
        except subprocess.TimeoutExpired:
            pass

    lines = stats('/tmp/tmpdir/fuzzer_stats')

    return render(request, 'run.html', {'stats': lines})
