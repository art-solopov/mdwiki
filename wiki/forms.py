from django import forms

from .models import Article

class ArticleForm(forms.ModelForm):

    """Article editing form"""

    class Meta:
        model = Article
        fields = ['body']


