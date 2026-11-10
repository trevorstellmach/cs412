# File: dadjokes/views.py
# Author: Trevor Stellmach, tstell@bu.edu (11/10/26)
# Description: defines views  for dadjokes

import random
from django.shortcuts import render
from django.views.generic import *
from .models import *


# Create your views here.
class ShowRandomJokeView(TemplateView):
    """view to display one random joke and one random picture"""

    template_name = "dadjokes/random_joke.html"

    def get_context_data(self, **kwargs):
        """override context data"""
        context = super().get_context_data(**kwargs)

        pks = Joke.objects.values_list('pk', flat=True)
        pk = random.choice(pks)
        context["joke"] = Joke.objects.get(pk=pk)

        pks = Picture.objects.values_list('pk', flat=True)
        pk = random.choice(pks)
        context["picture"] = Picture.objects.get(pk=pk)

        return context

class ShowAllJokesView(ListView):
    """view to display all jokes"""

    model = Joke
    template_name = "dadjokes/all_jokes.html"
    context_object_name = "jokes"

class ShowAllPicturesView(ListView):
    """view to display all pictures"""

    model = Picture
    template_name = "dadjokes/all_pictures.html"
    context_object_name = "pictures"

class ShowJokeView(DetailView):
    """view to display specific joke by pk"""

    model = Joke
    template_name = "dadjokes/show_joke.html"

    def get_context_data(self, **kwargs):
        """override context data"""
        context = super().get_context_data()
        pk = self.kwargs.get("pk")
        context["joke"] = Joke.objects.get(pk=pk)

        return context
    
class ShowPictureView(DetailView):
    """view to display specific picture by pk"""

    model = Picture
    template_name = "dadjokes/show_picture.html"

    def get_context_data(self, **kwargs):
        """override context data"""
        context = super().get_context_data()
        pk = self.kwargs.get("pk")
        context["picture"] = Picture.objects.get(pk=pk)

        return context