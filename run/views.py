import os
import shutil
import subprocess

from django.http import HttpResponseServerError
from django.shortcuts import render


PY_AFL_FUZZ_CMD = 'py-afl-fuzz'


def run(request):
    if not shutil.which(PY_AFL_FUZZ_CMD):
        return HttpResponseServerError()

    with open(os.devnull, 'w') as null:
        try:
            subprocess.call([
                PY_AFL_FUZZ_CMD, '-i', '.', '-o', '/tmp/tmpdir', 'python',
                'run/fuzz_cryptography.py'],
                timeout=10,
                stdout=null,
                stderr=null)
        except subprocess.TimeoutExpired:
            pass

    with open('/tmp/tmpdir/fuzzer_stats') as f:
        lines = f.readlines()
    lines = [i.split(':', 1) for i in lines]
    for i, x in enumerate(lines):
        lines[i][0] = lines[i][0].strip()
        lines[i][1] = lines[i][1].strip()

    return render(request, 'run.html', {'stats': lines})
