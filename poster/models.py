from django.db import models
from numpy import char

# Create your models here.


class events(models.Model):
    event_name = models.CharField(max_length=250)
    event_on_date = models.DateField()
    event_on_time = models.TimeField()
    about_event = models.TextField()
    tags = models.CharField(max_length=250)
    additional_info = models.TextField()
