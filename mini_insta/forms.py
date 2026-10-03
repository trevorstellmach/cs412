# File: mini_insta/forms.py
# Author: Trevor Stellmach, tstell@bu.edu (10/3/26)
# Description: mini_insta site forms file

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    """Form to create post"""

    class Meta:
        """associate this form with model from our database"""
        model = Post
        fields = ['timestamp', 'caption']
