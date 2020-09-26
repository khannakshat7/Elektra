from django.db import models

# Create your models here.

class electricity(models.Model):
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    is_solved = models.BooleanField(default=False)