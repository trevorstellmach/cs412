# File: mini_insta/views.py
# Author: Trevor Stellmach, tstell@bu.edu (09/26/26)
# Description: mini_insta site views file

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, Post
from .forms import CreatePostForm

# Create your views here.
class ProfileListView(ListView):
    """Subclass of ListView to show all profiles"""

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    """Subclass of DetailView to show one profile"""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

class PostDetailView(DetailView):
    """Subclass of DetailView to show one post"""

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

class CreatePostView(CreateView):
    """Subclass of CreateView to create a post"""

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"
