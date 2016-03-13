from django.db import models

# Create your models here.
class PollStat(models.Model):
	count = models.IntegerField()
	time = models.DateTimeField()
	name = models.CharField(max_length=256)
