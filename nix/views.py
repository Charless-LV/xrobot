from django.shortcuts   import render, redirect, reverse, get_object_or_404
from django.utils.translation   import ugettext_lazy as _
from .models import Task, Xperf, Perf
from .forms import TaskForm, XperfForm
from django.contrib import messages


def tasks(request, *args, **kwargs):
    template_name = 'tasks.html'
    tasks = Task.objects.all()
    print(tasks)
    ctx = {
        'tasks':tasks,
    }

    return render(request, template_name, ctx)


def task(request, tpk):
    template_name = 'task.html'
    task =  get_object_or_404(Task, pk=tpk)

    xperfs = Xperf.objects.filter(task=task)

    ctx = {
        'task':task,
        'xperfs':xperfs,
    }

    return render(request, template_name, ctx)






def task_create(request):
    user = request.user

    template_name = 'task_create.html'

    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            print('////////')
            task = form.save(commit=False)
            task.name = form.cleaned_data['name']
            task.mode = form.cleaned_data['mode']
            task.device = form.cleaned_data['device']
            task.description = form.cleaned_data['description']

            task.creator = user
            task.status = 0
            #print(task.name. task.mode, task.device, task.description, task.creator, task.status)
            task.save()
        messages.add_message(request, messages.SUCCESS,_('Create Task successfully!'), fail_silently=False)
        return redirect(reverse('tasks', args=[]))
    
    ctx = {
        'form':form,
    }

    return render(request, template_name, ctx)


def xperf_create(request, tpk):
    task = get_object_or_404(Task, pk=tpk)
    template_name='xperf_create.html'

    form = XperfForm(mode=task.mode)

    if request.method == 'POST':
        form = XperfForm(request.POST)
        if form.is_valid():
            xperf = form.save(commit=False)
            xperf.task = task
            xperf.ip = form.cleaned_data['ip']
            xperf.port = form.cleaned_data['port']
            # 自动调优模式下，如下参数为0， 遍历所有参数，取值为 Auto_Perf_settings
            xperf.buff = form.cleaned_data['buff']  if task.mode else 0
            xperf.parallel = form.cleaned_data['parallel']  if task.mode else 0
            xperf.interval = form.cleaned_data['interval']  if task.mode else 0
            xperf.seconds = form.cleaned_data['seconds']    if task.mode else 0
            xperf.save()
        messages.add_message(request, messages.SUCCESS,_('Xperf configure successfully!'), fail_silently=False)
        return redirect(reverse('task', args=[task.pk]))

    ctx = {
        'form':form,
    }

    return render(request, template_name, ctx)

def xperf(request, xpk):
    #res = {}
    template_name = 'xperf.html'
    xp = get_object_or_404(Xperf, pk=xpk)
    #res = xp.run()
    #record = Perf(xp, result=res)
    
    ctx = {
        'xperf':xp,
    }

    return render(request, template_name, ctx)


def xperf_run(request, xpk):
    template_name= 'xperf_run.html'
    xperf = get_object_or_404(Xperf, pk=xpk)
    
    boots =xperf.bootstrap()
    
    xr = xperf.run()
    print(xr, '////////')
    pf = Perf.objects.create(xperf=xperf, result=xr)
    
    ctx = {
        'xperf':xperf,
        'create_time':xperf.create_time,
        'boots':boots,
	'status': xr if xr else 'RUNING..',
    }

    return render(request, template_name, ctx)



def xperf_stop(request, xpk):
    template_name = 'xperf_stop.html'
    xperf = get_object_or_404(Xperf, pk=xpk)
    boots =xperf.bootstrap()      
    stp = xperf.stop()
    
    ctx = {
        'xperf': xperf,
        'boots': boots,
        'create_time':xperf.create_time,
        'status':stp if stp else 'stopped',

    }

    return render(request, template_name, ctx)



