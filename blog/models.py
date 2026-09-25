from django.db import models

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