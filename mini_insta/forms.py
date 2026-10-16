# File: mini_insta/forms.py
# Author: Trevor Stellmach, tstell@bu.edu (10/3/26)
# Description: defines form classes for mini_insta

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    """Form to create post"""

    class Meta:
        """associate this form with model from our database"""
        model = Post
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    """Form to update profile"""

    class Meta:
        """associate form with model from our database"""
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']

class UpdatePostForm(forms.ModelForm):
    """Form to update post"""

    class Meta:
        model = Post
        fields = ['caption']