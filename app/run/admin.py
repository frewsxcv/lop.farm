from django.contrib import admin

from run.models import AflRun


class AflRunAdmin(admin.ModelAdmin):
    pass

admin.site.register(AflRun, AflRunAdmin)
