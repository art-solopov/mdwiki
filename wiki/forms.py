from django import forms

from .models import Article

def _article_form_widget():
    return forms.Textarea(
        attrs={'class': 'form-control', 'rows': 30}
        )

class ArticleForm(forms.ModelForm):

    """Article editing form"""

    class Meta:
        model = Article
        fields = ['body']
        body_widget = _article_form_widget()
        widgets = {
            'body': body_widget
        }

class NewArticleForm(forms.Form):

    """New article form"""

    name = forms.CharField(label='Article name', max_length=1100)
    slug = forms.SlugField(label='Article slug', max_length=1100)
    body = forms.CharField(label='Article body', widget=_article_form_widget())
