from django.db import models

# Create your models here.

class electricity(models.Model):
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    is_solved = models.BooleanField(default=False)

#Model for contact
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField( max_length=254)
    phone = models.CharField(max_length=13)
    message = models.TextField()