from datetime import datetime
import os
import shutil
import subprocess

from celery import task
from django.db import transaction
from django.utils import timezone

from run.afl_utils import stats
from run.models import AflRun, Run


PY_AFL_FUZZ_CMD = 'py-afl-fuzz'
AFL_OUTPUT_DIR = '/tmp/tmpdir'

# FIXME: username should be randomly generated? incorporate user id / username?
_USERNAME = 'meow'


@task
def run_afl(run_id, duration):
    assert isinstance(run_id, int)
    assert isinstance(duration, int)

    assert not os.path.exists(AFL_OUTPUT_DIR)

    subprocess.run(['adduser', _USERNAME, '--gecos', '""',
                    '--disabled-password']).check_returncode()

    root_uid = os.getuid()

    run = subprocess.run(['id', '-u', _USERNAME], stdout=subprocess.PIPE)
    run.check_returncode()
    uid = int(run.stdout)
    assert uid != root_uid

    os.seteuid(uid)

    Run.objects.filter(id=run_id).update(started_on=timezone.now())

    # TODO: create home directory for user, run code inside home directory
    with open(os.devnull, 'w') as null:
        try:
            subprocess.run([
                PY_AFL_FUZZ_CMD, '-i', '.', '-o', AFL_OUTPUT_DIR,
                '/srv/venv/bin/python', 'run/fuzz_cryptography.py'],
                timeout=duration,
                stdout=null,
                stderr=null)
        except subprocess.TimeoutExpired:
            pass

    lines = stats(os.path.join(AFL_OUTPUT_DIR, 'fuzzer_stats'))

    shutil.rmtree(AFL_OUTPUT_DIR)

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

    with transaction.atomic():
        AflRun.objects.create(run_id=run_id, **model_args)
        Run.objects.filter(id=run_id).update(completed_on=timezone.now())

    os.seteuid(root_uid)

    subprocess.run(['userdel', '-r', _USERNAME]).check_returncode()
