import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation   import ugettext_lazy as _

Auto_Perf_Settings = {
    'buffsize':['32k', '64k', '128k','256k','512k','1024k']
}


class Task(models.Model):
    '''针对某硬件设备创建测试任务'''
    STATUS=(
        (0, _('Created')),
        (1, _('Running')),
        (2, _('Error/Suspend')),
        (3, _('Success')),
    )

    MODE = (
        (0, 'Auto Perf'),
        (1, 'Custome')
    )

    name    = models.CharField(max_length=100, verbose_name='Task Name')
    mode    = models.PositiveIntegerField(_("Mode"))
    creator = models.ForeignKey(User, related_name='Creator', on_delete=models.CASCADE)
    status  = models.PositiveIntegerField(verbose_name='Status', choices=STATUS, default=0)
    device  = models.CharField(max_length=100, verbose_name='Device')
    description = models.CharField(max_length=5000, verbose_name='Description')
    create_time = models.DateTimeField(_('Create time'),auto_now_add=True)

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    def __str__(self):
        return '{}: {}'.format(self.device, self.name)

    def get_absolute_url(self):
        return reverse("Task_detail", kwargs={"pk": self.pk})


class XperfAbstractModel(models.Model):
    task= models.ForeignKey(Task, related_name='Task', on_delete=models.CASCADE)
    ip  = models.GenericIPAddressField(_("IP Address"),)
    port= models.PositiveIntegerField(_("Port"),)
    create_time = models.DateTimeField(_("Create Time"),auto_now_add=True)
    start_time  = models.DateTimeField(_("Start Time"),auto_now_add=False, null=True, blank=True)
    Stop_time   = models.DateTimeField(_("Stop Time"),auto_now_add=True)

    class Meta:
        abstract = True


class Xperf(XperfAbstractModel):
    SIZE = (
        (32, '32k'),
        (64, '64k'),
        (128, '128k'),
        (256, '256k'),
        (512, '512k'),
        (1024, '1024k'),
    )

    buff= models.PositiveIntegerField(_("Buff Size"), )
    parallel= models.PositiveIntegerField(_("Parallel"),)
    interval= models.PositiveIntegerField(_("Interval"), )
    seconds = models.PositiveIntegerField(_("seconds"),)
    

    class Meta:
        verbose_name = _("xperf")
        verbose_name_plural = _("xperfs")
    
    #@property
    def bootstrap(self):
        print('///////////')
        boots = 'iperf3 -c {} -p {} -w {}k -P {} -i {} -t {}'.format(self.ip, self.port, self.buff, self.parallel, self.interval, self.seconds)
        print(boots)
        #print(type(self.port), type(self.buff), type(self.interval), type(self.parallel), type(self.seconds), type(self.ip))
        return boots

    def __str__(self):
        return 'Task:{} / Xperf: {}:{}'.format(self.task, self.ip, self.port)

    def get_absolute_url(self):
        return reverse("xperf_detail", kwargs={"pk": self.pk})


    def run(self):
        res =  os.popen(self.bootstrap() +'|grep -E \'SUM|sec\'|tail -1|awk -F \']\' \'{ print $2}\'|awk \'{ print %5} \'').read().strip()
        return res

    def auto_run(self):
        return

    def stop(self):
        return



# class AutoPerf(XperfAbstractModel):
#     def __init__(self, *args, **kwargs):
#         self.ip = kwargs.pop('ip')
#         self.port = kwargs.pop('port')
#         self.buff = kwargs.pop('buff')
#         self.parallel = kwargs.pop('parallel')


class Perf(models.Model):
    xperf = models.ForeignKey(Xperf, related_name='Xperf', on_delete=models.CASCADE)
    result= models.FloatField(_("Result"))
    time_stamp  = models.DateTimeField(_("Time Stamp"), auto_now=True)
    

    class Meta:
        verbose_name = _("Perf")
        verbose_name_plural = _("Perfs")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Perf_detail", kwargs={"pk": self.pk})
