from django.shortcuts import render

from run.models import AflRun


def landing(request):
    runs = AflRun.objects.order_by('-start_time')
    return render(request, 'landing.html', {
        "runs": runs,
    })
