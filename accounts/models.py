from django.db import models

# Create your models here.
class Account(models.Model):
    name = models.CharField('id', max_length=255, unique=True)
    password = models.CharField('password', max_length=255)

class Proxy(models.Model):
	url = models.CharField(max_length=255, unique=True)
	rate = models.IntegerField(blank=True)