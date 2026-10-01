from django.db import models
from django.urls import reverse

# Create your models here.
class Article(models.Model):

    # define data attributes of Article object
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(blank=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f'{self.title} by {self.author}' 

    def get_absolute_url(self):
        """return a url to display one instance of this object"""
        return reverse('article', kwargs={'pk':self.pk})