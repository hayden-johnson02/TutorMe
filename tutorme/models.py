from django.db import models

# Create your models here.

# temporary model
class Dummy(models.Model):
    dummy = models.CharField(max_length = 1)