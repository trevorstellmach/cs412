# File: mini_insta/views.py
# Author: Trevor Stellmach, tstell@bu.edu (09/26/26)
# Description: defines view classes and logic for mini_insta

from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse
from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.
class LogoutConfirmationView(TemplateView):
    """Subclass of TemplateView to show logout confirmation"""
    template_name = 'mini_insta/logged_out.html'

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

class LoggedInProfileView(LoginRequiredMixin, DetailView):
    """Subclass of DetailView to show profile of logged in user"""
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        """returns necessary Profile object for logged in user"""
        return Profile.objects.get(user=self.request.user)

class PostDetailView(DetailView):
    """Subclass of DetailView to show one post"""

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

class CreatePostView(LoginRequiredMixin, CreateView):
    """Subclass of CreateView to create a post"""

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_login_url(self):
        """return URL of login page"""
        return reverse('login')

    def get_object(self):
        """returns necessary Profile object for logged in user"""
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self):
        "Return the dictionary of context variables for use in the template"

        # calling superclass method
        context = super().get_context_data()

        profile = self.get_object()

        context['profile'] = profile
        return context

    def form_valid(self, form):
        """handles form submission"""

        profile = self.get_object()
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

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Subclass of UpdateView that updates Profiles"""

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

    def get_login_url(self):
        """return URL of login page"""
        return reverse('login')

    def get_object(self):
        """returns necessary Profile object for logged in user"""
        return Profile.objects.get(user=self.request.user)

    def form_valid(self, form):
        """handles form submission"""

        profile = self.get_object()
        form.instance.profile = profile

        response = super().form_valid(form)

        return response

class DeletePostView(LoginRequiredMixin, DeleteView):
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

class UpdatePostView(LoginRequiredMixin, UpdateView):
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

class ShowFeedView(LoginRequiredMixin, DetailView):
    """Subclass of DetailView that shows a user's Feed"""

    model = Profile
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'profile'

    def get_login_url(self):
        """return URL of login page"""
        return reverse('login')

    def get_object(self):
        """returns necessary Profile object for logged in user"""
        return Profile.objects.get(user=self.request.user)

class SearchView(LoginRequiredMixin, ListView):
    """Subclass of ListView that allows for searching posts and profiles"""

    model = Profile
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'profile'

    def get_login_url(self):
        """return URL of login page"""
        return reverse('login')

    def get_object(self):
        """returns necessary Profile object for logged in user"""
        return Profile.objects.get(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        """Handles dispatch for requests"""
        if 'query' in self.request.GET:     # check if query is in the request
            return super().dispatch(request, *args, **kwargs)
        else:
           # take to search page if not
            profile = self.get_object()
            return render(request, template_name='mini_insta/search.html', context={'profile': profile})

    def get_queryset(self):
        """Returns data that matches passed in query"""

        query = self.request.GET["query"]

        result = Post.objects.filter(caption__contains=query)   # get posts that contain the query in the caption

        return result

    def get_context_data(self, **kwargs):
        """Return the dictionary of context variables for use in the template"""

        context = super().get_context_data()

        query = self.request.GET["query"]

        profile = self.get_object()
        context['profile'] = profile

        context['query'] = query
        context['posts'] = self.get_queryset()

        # get profiles with the query in username, display name, or bio
        profiles = Profile.objects.filter(username__contains=query) | Profile.objects.filter(display_name__contains=query) | Profile.objects.filter(bio_text__contains=query)
        context['profiles'] = profiles

        return context

class CreateProfileView(CreateView):
    """Subclass of CreateView that shows/processes registration form to make a new user"""

    template_name = 'mini_insta/create_profile_form.html'
    form_class = CreateProfileForm
    model = Profile

    def get_success_url(self):
        """URL to redirect to after making an account"""
        return reverse('login')

    def get_context_data(self, **kwargs):
        """returns dictionary of context data for use in template"""

        context = super().get_context_data()
        context['user_creation_form'] = UserCreationForm()

        return context

    def form_valid(self, form):
        """handles form submission"""

        print("LOOK HERE", self.request.POST)

        # rebuild user_creation_form
        user_form = UserCreationForm(self.request.POST)

        if user_form.is_valid():
            # create User object
            user = user_form.save()
            form.instance.user = user

            # log in user
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        response = super().form_valid(form)

        return response

        

