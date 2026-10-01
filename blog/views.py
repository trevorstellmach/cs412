from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Article
from .forms import CreateArticleForm
import random

# Create your views here.
class ShowAllView(ListView):

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"

class ArticleView(DetailView):

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

class RandomArticleView(DetailView):

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

    def get_object(self):

        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article

class CreateArticleView(CreateView):
    '''view to create now article
    1. display HTML form to user (GET)
    2. process form submission and store new Article object (POST)
    '''

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"
