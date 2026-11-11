# File: dadjokes/urls.py
# Author: Trevor Stellmach, tstell@bu.edu (11/10/26)
# Description: defines URL paths for dadjokes

from django.urls import path
from django.conf import settings
from . import views
from .views import *

urlpatterns = [
    path('', ShowRandomJokeView.as_view(), name="main"),
    path('random', ShowRandomJokeView.as_view(), name="show_random"),
    path('jokes', ShowAllJokesView.as_view(), name="show_all_jokes"),
    path('joke/<int:pk>', ShowJokeView.as_view(), name="show_joke"),
    path('pictures', ShowAllPicturesView.as_view(), name="show_all_pictures"),
    path('picture/<int:pk>', ShowPictureView.as_view(), name="show_picture"),

    # API Paths
    path(r'api/', RandomJokeAPIView.as_view()),
    path(r'api/random', RandomJokeAPIView.as_view()),
    path(r'api/jokes', JokeListAPIView.as_view()),
    path(r'api/joke/<int:pk>', JokeDetailAPIView.as_view()),
    path(r'api/pictures', PictureListAPIView.as_view()),
    path(r'api/picture/<int:pk>', PictureDetailAPIView.as_view()),
    path(r'api/random_picture', RandomPictureDetailAPIView.as_view())
]