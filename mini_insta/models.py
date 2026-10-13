# File: mini_insta/models.py
# Author: Trevor Stellmach, tstell@bu.edu (09/25/26)
# Description: mini_insta site models file

from django.db import models
from django.urls import reverse

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

    def get_absolute_url(self):
        """returns url back to profile page"""
        return reverse('show_profile', kwargs={'pk': self.pk})

    def get_followers(self):
        """returns a list of a given profile's followers"""
        followers = Follow.objects.filter(profile=self)
        follower_accounts = []
        for x in list(followers):
            follower_accounts += [x.follower_profile]

        return follower_accounts

    def get_num_followers(self):
        """returns number of followers"""
        num = self.get_followers()
        return len(num)

    def get_following(self):
        """returns list of accounts self is following"""
        following = Follow.objects.filter(follower_profile = self)
        following_accounts = []
        for x in following:
            following_accounts += [x.profile]

        return following_accounts

    def get_num_following(self):
        """returns number of following"""
        return len(self.get_following())


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

    def get_absolute_url(self):
        """returns url back to post page"""
        return reverse('show_post', kwargs={'pk': self.pk})


class Photo(models.Model):
    """Defines Photo model"""

    # attributes
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(blank=True)
    image_file = models.ImageField(upload_to="mini_insta/", blank=True)

    def get_image_url(self):
        """returns image url"""
        
        if self.image_url:
            return self.image_url
        elif self.image_file:
            return self.image_file.url
        else:
            return "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSKKzAcX4o85e8WqOLI80UB1H5sOOUlwW8XKy8EIxl3Q&s=10"

    def __str__(self):
        """Reformats string representation of Photo model"""
        
        if self.image_url:
            return f'{self.post}, {self.image_url}, {self.timestamp}'
        elif self.image_file:
            return f'{self.post}, {self.image_file.url}, {self.timestamp}'
        else:
            return f'{self.post}, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSKKzAcX4o85e8WqOLI80UB1H5sOOUlwW8XKy8EIxl3Q&s=10, {self.timestamp}'

class Follow(models.Model):
    """Defines Follow model"""

    #attributes
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String rep of the Follow model"""

        return f'{self.follower_profile.display_name} follows {self.profile.display_name}'