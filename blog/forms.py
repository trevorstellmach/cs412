from django import forms
from .models import Article

class CreateArticleForm(forms.ModelForm):
    '''Form to add article to database'''

    class Meta:
        '''associate this form with a model from our database'''
        model = Article
        fields = ['author', 'title', 'text', 'image_url']