from django.db import models

# Create your models here.

class Phrase(models.Model):
	phrase = models.CharField(max_length=500)
	translated = models.CharField(max_length=1000)
	comment = models.CharField(max_length=1000)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)	
