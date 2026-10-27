# File: voter_analytics/urls.py
# Author: Trevor Stellmach, tstell@bu.edu (10/27/26)
# Description: defines URL paths for voter_analytics

from django.urls import path
from django.conf import settings
from . import views
from .views import *

urlpatterns = [
    path('', VotersListView.as_view(), name="voters"), # voters page
]