import os
import shutil
import subprocess
from datetime import datetime

from django.http import HttpResponseServerError
from django.shortcuts import render
from django.utils import timezone

from run.afl_utils import stats
from run.models import AflRun


PY_AFL_FUZZ_CMD = 'py-afl-fuzz'


def run(request):
    if not shutil.which(PY_AFL_FUZZ_CMD):
        return HttpResponseServerError()

    with open(os.devnull, 'w') as null:
        try:
            subprocess.run([
                PY_AFL_FUZZ_CMD, '-i', '.', '-o', '/tmp/tmpdir',
                '/srv/venv/bin/python', 'run/fuzz_cryptography.py'],
                timeout=10,
                stdout=null,
                stderr=null)
        except subprocess.TimeoutExpired:
            pass

    lines = stats('/tmp/tmpdir/fuzzer_stats')

    model_args = {
        'start_time': timezone.make_aware(
            datetime.fromtimestamp(int(lines.pop('start_time')))),
        'last_update': timezone.make_aware(
            datetime.fromtimestamp(int(lines.pop('last_update')))),
        'fuzzer_pid': int(lines.pop('fuzzer_pid')),
        'cycles_done': int(lines.pop('cycles_done')),
        'execs_done': int(lines.pop('execs_done')),
        'execs_per_sec': float(lines.pop('execs_per_sec')),
        'paths_total': int(lines.pop('paths_total')),
        'paths_favored': int(lines.pop('paths_favored')),
        'paths_found': int(lines.pop('paths_found')),
        'paths_imported': int(lines.pop('paths_imported')),
        'max_depth': int(lines.pop('max_depth')),
        'cur_path': int(lines.pop('cur_path')),
        'pending_favs': int(lines.pop('pending_favs')),
        'pending_total': int(lines.pop('pending_total')),
        'variable_paths': int(lines.pop('variable_paths')),
        'bitmap_cvg': int(
            lines.pop('bitmap_cvg').rstrip('%').replace('.', '')),
        'unique_crashes': int(lines.pop('unique_crashes')),
        'unique_hangs': int(lines.pop('unique_hangs')),
        'last_path': timezone.make_aware(
            datetime.fromtimestamp(int(lines.pop('last_path')))),
        'last_crash': timezone.make_aware(
            datetime.fromtimestamp(int(lines.pop('last_crash')))),
        'last_hang': timezone.make_aware(
            datetime.fromtimestamp(int(lines.pop('last_hang')))),
        'exec_timeout': int(lines.pop('exec_timeout')),
        'afl_version': lines.pop('afl_version'),
    }

    # Items we don't care about for the time being
    del lines['afl_banner']
    del lines['command_line']

    assert not lines

    AflRun.objects.create(**model_args)

    return render(request, 'run.html')
