# blog/urls.py
from django.urls import path
from django.conf import settings
from . import views
from .views import *

urlpatterns = [
    path('', RandomArticleView.as_view(), name="show_all"),
    path('show_all', ShowAllView.as_view(), name="show_all"),
    path('article/<int:pk>', ArticleView.as_view(), name='article'),
    path('article/create', CreateArticleView.as_view(), name="create_article")
]