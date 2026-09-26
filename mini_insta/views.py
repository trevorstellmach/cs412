# File: mini_insta/views.py
# Author: Trevor Stellmach, tstell@bu.edu (09/26/26)
# Description: mini_insta site views file

from django.shortcuts import render
from django.views.generic import ListView
from .models import Profile

# Create your views here.
class ProfileListView(ListView):
    """Subclass of ListView to show all profiles"""

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"
