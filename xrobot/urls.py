from django.contrib import admin
from django.urls import path, include
from nix import views

urlpatterns = [
    path('tasks', views.tasks, name='tasks'),
    path('task/<int:tpk>', views.task, name='task'),
    path('task/create', views.task_create, name='task_create'),

    path('xperf/<int:tpk>/create', views.xperf_create, name='xperf_create'),
    path('xperf/<int:xpk>', views.xperf, name='xperf'),
    path('xperf/<int:xpk>/run', views.xperf_run, name='xperf_run'),
    path('xperf/<int:xpk>/stop', views.xperf_stop, name='xperf_stop'),

    path('admin/', admin.site.urls),
]


