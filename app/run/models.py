from django.db import models


class Run(models.Model):
    # repository = models.ForeignKey(Repository)
    queued_on = models.DateTimeField(auto_now_add=True)
    started_on = models.DateTimeField(null=True)
    completed_on = models.DateTimeField(null=True)


class AflRun(models.Model):
    run = models.OneToOneField(Run)

    start_time = models.DateTimeField(
        help_text='Start time')
    last_update = models.DateTimeField(
        help_text='Last time stats were updated')
    fuzzer_pid = models.PositiveIntegerField(
        help_text='Process ID of the run')
    cycles_done = models.PositiveIntegerField(
        help_text='Queue round counter')
    execs_done = models.PositiveIntegerField(
        help_text='Total execve() calls')
    execs_per_sec = models.FloatField(
        help_text='Average execve() calls per second')
    paths_total = models.PositiveIntegerField(
        help_text='Total number of queued testcases')
    paths_favored = models.PositiveIntegerField(
        help_text='Paths deemed favorable')
    paths_found = models.PositiveIntegerField(
        help_text='Items discovered during this run')
    paths_imported = models.PositiveIntegerField(
        help_text='Items imported via -S')
    max_depth = models.PositiveIntegerField(
        help_text='Max path depth')
    cur_path = models.PositiveIntegerField(
        help_text='Current queue entry ID')
    pending_favs = models.PositiveIntegerField(
        help_text='Pending favored paths')
    pending_total = models.PositiveIntegerField(
        help_text='Queued but not done yet')
    variable_paths = models.PositiveIntegerField(
        help_text='Testcases with variable behavior')
    bitmap_cvg = models.PositiveSmallIntegerField(
        help_text='Bitmap coverage (percent)')
    unique_crashes = models.PositiveIntegerField(
        help_text='Crashes with unique signatures')
    unique_hangs = models.PositiveIntegerField(
        help_text='Hangs with unique signatures')
    last_path = models.DateTimeField(
        help_text='Time for most recent path')
    last_crash = models.DateTimeField(
        help_text='Time for most recent crash')
    last_hang = models.DateTimeField(
        help_text='Time for most recent hang')
    exec_timeout = models.PositiveIntegerField(
        help_text='Timeout for each run (ms)')
    afl_version = models.CharField(
        max_length=10,
        help_text='Version of AFL')
