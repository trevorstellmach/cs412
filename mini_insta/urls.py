# File: mini_insta/urls.py
# Author: Trevor Stellmach, tstell@bu.edu (09/25/26)
# Description: defines URL paths for mini_insta

from django.urls import path
from django.conf import settings
from . import views
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles"), # home page
    path('profile', LoggedInProfileView.as_view(), name="logged_in_profile"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"), # profile page
    path('post/<int:pk>', PostDetailView.as_view(), name="show_post"), # individual post page
    path('profile/create_post', CreatePostView.as_view(), name="create_post"), # create post page
    path('profile/update', UpdateProfileView.as_view(), name="update_profile"), # update profile page
    path('post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"), # delete post page
    path('post/<int:pk>/update', UpdatePostView.as_view(), name="update_post"), # update post page
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name="show_followers"), # followers page
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name="show_following"), # following page
    path('profile/feed', ShowFeedView.as_view(), name="show_feed"), # feed page
    path('profile/search', SearchView.as_view(), name="show_search"), # search page
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name="login"), # login page
    path('logout/', auth_views.LogoutView.as_view(next_page="logout_confirmation"), name="logout"), # logout page
    path('logout_confirmation', LogoutConfirmationView.as_view(), name="logout_confirmation"), # logout confirmation page
    path('create_profile/', CreateProfileView.as_view(), name="create_profile"), # user registration page
    path('profile/<int:pk>/follow', CreateFollowView.as_view(), name="follow"), # follow
    path('profile/<int:pk>/delete_follow', DeleteFollowView.as_view(), name="delete_follow"), # unfollow
    # path('post/<int:pk>/like', CreateLikeView.as_view(), name="like"), # like
    # path('post/<int:pk>/delete_like', DeleteLikeView.as_view(), name="delete_like") # remove like


]