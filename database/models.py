from django.db import models

# Create your models here.
class users(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class mobiles(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/devices/')
    price = models.IntegerField()
    description = models.TextField()
    category = models.CharField(max_length=100)

class ipads(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/devices/')
    price = models.IntegerField()
    description = models.TextField()
    category = models.CharField(max_length=100)

class cart(models.Model):
    name = models.CharField(max_length=100)
    # Array for storing multiple items
    items = models.TextField()

class orders(models.Model):
    name = models.CharField(max_length=100)
    count = models.IntegerField()