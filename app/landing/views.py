from django.shortcuts import render

from run.models import AflRun, Run


def landing(request):
    pending_runs = Run.objects.filter(started_on=None, completed_on=None)
    active_runs = Run.objects.exclude(started_on=None).filter(completed_on=None)
    afl_runs = AflRun.objects.order_by('-start_time')
    return render(request, 'landing.html', {
        "afl_runs": afl_runs,
        "active_runs": active_runs,
        "pending_runs": pending_runs,
    })
