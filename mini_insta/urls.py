# File: mini_insta/urls.py
# Author: Trevor Stellmach, tstell@bu.edu (09/25/26)
# Description: mini_insta site URL file

from django.urls import path
from django.conf import settings
from . import views
from .views import ProfileListView

urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles")
]