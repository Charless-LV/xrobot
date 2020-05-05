from django.contrib import admin
from .models import Xperf, Perf, Task

class PerfAdmin(admin.ModelAdmin):
    list_display = ('xperf', 'result', 'time_stamp')

admin.site.register(Xperf)
admin.site.register(Perf, PerfAdmin)
admin.site.register(Task)
