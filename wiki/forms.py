from django import forms

from .models import Article


class ArticleForm(forms.ModelForm):

    """Article editing form"""

    class Meta:
        model = Article
        fields = ['body']
        body_widget = forms.Textarea(
            attrs={'class': 'form-control', 'rows': 30}
        )
        widgets = {
            'body': body_widget
        }

class NewArticleForm(forms.ModelForm):

    """New article form"""

    # class Meta(ArticleForm.Meta):
    #     fields = ['name', 'body']
    #     widgets = {
    #         'body': ArticleForm.Meta.body_widget,
    #         'name': forms.TextInput(attrs={'class': 'form-control'})
    #     }
