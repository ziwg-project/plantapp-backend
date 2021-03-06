from django.db import models
from django.contrib.auth import get_user_model
from django_celery_beat.models import IntervalSchedule, PeriodicTask

USER_MODEL = get_user_model()


class Location(models.Model):
    LOC_OPTIONS = (
        ('O', 'OUTSIDE'),
        ('I', 'INSIDE')
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=1, choices=LOC_OPTIONS)
    owner_fk = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)


class Plant(models.Model):
    name = models.CharField(max_length=100)
    sci_name = models.CharField(blank=True, max_length=100)
    image = models.ImageField(blank=True)
    loc_fk = models.ForeignKey(Location, on_delete=models.CASCADE)


class Reminder(models.Model):
    INTRVL_OPTIONS = (
        ('S', 'SECONDS'),
        ('M', 'MINUTES'),
        ('H', 'HOURS'),
        ('D', 'DAYS'),
        ('W', 'WEEKS'),
        ('m', 'MONTHS'),
        ('Y', 'YEARS')
    )
    text = models.TextField()
    base_tmstp = models.DateTimeField()
    intrvl_num = models.IntegerField()
    intrvl_type = models.CharField(max_length=1, choices=INTRVL_OPTIONS)
    plant_fk = models.ForeignKey(Plant, on_delete=models.CASCADE)
    notification_task = models.ForeignKey(PeriodicTask, on_delete=models.CASCADE, default=None)

    def delete(self, using=None, keep_parents=False):
        if self.notification_task:
            self.notification_task.delete()
        super().delete(using, keep_parents)


class Note(models.Model):
    text = models.TextField()
    plant_fk = models.ForeignKey(Plant, on_delete=models.CASCADE)


class Log(models.Model):
    LOG_OPTIONS = (
        ('D', 'DONE'),
        ('S', 'SKIPPED')
    )
    log_type = models.CharField(max_length=1, choices=LOG_OPTIONS)
    log_tmstp = models.DateTimeField()
    reminder_fk = models.ForeignKey(Reminder, on_delete=models.CASCADE)
