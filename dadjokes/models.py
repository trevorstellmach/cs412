# File: dadjokes/models.py
# Author: Trevor Stellmach, tstell@bu.edu (11/10/26)
# Description: includes model classes and methods for dadjokes

from django.db import models

# Create your models here.
class Joke(models.Model):
    """Stores instance of a joke"""
    text = models.TextField()
    name = models.TextField()
    timestamp = models.TimeField(auto_now=True)

class Picture(models.Model):
    """Stores instance of a picture"""
    image_url = models.URLField()
    name = models.TextField()
    timestamp = models.TimeField(auto_now=True)