# File: mini_insta/models.py
# Author: Trevor Stellmach, tstell@bu.edu (09/25/26)
# Description: mini_insta site models file

from django.db import models

# Create your models here.
class Profile(models.Model):
    """Defines Profile model"""

    # attributes
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateField(blank=True)

    def __str__(self):
        """Reformats string representation of model"""

        return f'{self.username}, {self.display_name}, {self.bio_text}, {self.join_date}'
