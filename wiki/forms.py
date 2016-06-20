from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from wiki.models import Article, Alias

def _article_form_widget():
    return forms.Textarea(
        attrs={'rows': 30}
        )

class ArticleForm(forms.ModelForm):

    """Article editing form"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'article_edit_form' # TODO bind to article pk
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Article
        fields = ['body']
        body_widget = _article_form_widget()
        widgets = {
            'body': body_widget
        }

class NewArticleForm(forms.Form):

    """New article form"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id  = 'new_article_form'

        self.helper.add_input(Submit('submit', 'Submit'))

    name = forms.CharField(label='Article name', max_length=1100)
    body = forms.CharField(label='Article body', widget=_article_form_widget())

class AliasForm(forms.ModelForm):

    """Alias form"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'alias_form'

        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Alias
        fields = ['name']
