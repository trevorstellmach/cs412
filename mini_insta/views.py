# File: mini_insta/views.py
# Author: Trevor Stellmach, tstell@bu.edu (09/26/26)
# Description: mini_insta site views file

from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm

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

    def get_context_data(self):
        "Return the dictionary of context variables for use in the template"

        # calling superclass method
        context = super().get_context_data()

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        context['profile'] = profile
        return context

    def form_valid(self, form):
        """handles form submission"""

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        form.instance.profile = profile

        timestamp = datetime.now()
        form.instance.timestamp = timestamp

        response = super().form_valid(form)

        files = self.request.FILES.getlist('image_file')
        print("MY FILES: ", files)
        for img in files:
            Photo.objects.create(
                post = self.object,
                #image_url = self.request.POST["img_url"],
                image_file = img,
                timestamp = datetime.now()
            )

        return response

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Post.'''

        # go to post after it's been created
        return reverse('show_post', kwargs={'pk': self.object.pk})

class UpdateProfileView(UpdateView):
    """Subclass of UpdateView that updates Profiles"""

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

class DeletePostView(DeleteView):
    """Subclass of DeleteView that deletes Posts"""

    model = Post
    template_name = 'mini_insta/delete_post_form.html'

    def get_context_data(self, **kwargs):
        """Return the dictionary of context variables for use in the template"""

        context = super().get_context_data()

        post = self.object
        profile = post.profile

        context['profile'] = profile
        context['post'] = post
        return context

    def get_success_url(self):
        '''Provide a URL to redirect to after deleting a post'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class UpdatePostView(UpdateView):
    """Subclass of UpdateView that updates posts"""

    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

class ShowFollowersDetailView(DetailView):
    """Subclass of DetailView that shows followers"""

    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'

class ShowFollowingDetailView(DetailView):
    """Subclass of DetailView that shows following"""

    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'

class ShowFeedView(DetailView):
    """Subclass of DetailView that shows a user's Feed"""

    model = Profile
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'profile'

class SearchView(ListView):
    """Subclass of ListView that allows for searching posts and profiles"""

    model = Profile
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'profile'

    def dispatch(self, request, *args, **kwargs):
        """Handles dispatch for requests"""
        print(self.request.GET)
        if 'query' in self.request.GET:
            return super().dispatch(request, *args, **kwargs)
        else:
            pk = self.kwargs['pk']
            profile = Profile.objects.get(pk=pk)
            return render(request, template_name='mini_insta/search.html', context={'profile': profile})

    def get_queryset(self):
        """Returns data that matches passed in query"""

        query = self.request.GET["query"]

        result = Post.objects.filter(caption__contains=query)

        return result

    def get_context_data(self, **kwargs):
        """Return the dictionary of context variables for use in the template"""

        context = super().get_context_data()

        query = self.request.GET["query"]

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile

        context['query'] = query
        context['posts'] = self.get_queryset()

        profiles = Profile.objects.filter(username__contains=query) | Profile.objects.filter(display_name__contains=query) | Profile.objects.filter(bio_text__contains=query)
        context['profiles'] = profiles

        return context





