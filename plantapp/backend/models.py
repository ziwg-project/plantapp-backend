from django.db import models
from django.contrib.auth import get_user_model

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
        ('W', 'WEEKS')
    )
    text = models.TextField()
    base_tmstp = models.TimeField()
    intrvl_num = models.IntegerField()
    intrvl_type = models.CharField(max_length=1, choices=INTRVL_OPTIONS)
    plant_fk = models.ForeignKey(Plant, on_delete=models.CASCADE)
