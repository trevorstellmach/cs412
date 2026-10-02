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

    def get_all_posts(self):
        """returns all posts for a given profile"""
        posts = Post.objects.filter(profile=self).order_by('timestamp')
        return posts

class Post(models.Model):
    """Defines Post model"""

    # attributes
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(blank=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        """Reformats string representation of Post model"""
        return f'{self.profile.display_name}, {self.timestamp}, {self.caption}'

    def get_all_photos(self):
        """returns all photos for a given post"""
        photos = Photo.objects.filter(post=self)
        return photos

    def get_cover_photo(self):
        """returns photo to be used for posts grid"""

        photo = Photo.objects.filter(post=self).first()
        return photo


class Photo(models.Model):
    """Defines Photo model"""

    # attributes
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(blank=True)

    def __str__(self):
        """Reformats string representation of Photo model"""
        return f'{self.post}, {self.image_url}, {self.timestamp}'