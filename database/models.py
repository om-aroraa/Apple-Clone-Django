from django.db import models

# Create your models here.
class users(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class mobiles(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/devices/')
    price = models.IntegerField()
    keyfeature = models.TextField()

class ipads(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/devices/')
    price = models.IntegerField()
    keyfeature = models.TextField()

class MacBooks(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/devices/')
    price = models.IntegerField()
    keyfeature = models.TextField()

class cart(models.Model):
    name = models.CharField(max_length=100)
    # Array for storing multiple items
    items = models.TextField(null=True)