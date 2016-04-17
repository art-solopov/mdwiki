from django.forms import ModelForm, CharField, PasswordInput
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class UserRegisterForm(ModelForm):

    password = CharField(widget=PasswordInput, required=True)
    password_confirmation = CharField(widget=PasswordInput,
                                      required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'user_register_form'
        self.helper.form_method = 'POST'

        self.helper.add_input(Submit('submit', 'Register'))

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get('password')
        pwd_conf = cleaned_data.get('password_confirmation')
        if pwd and pwd_conf and pwd != pwd_conf:
            self.add_error('password_confirmation', 'Not equal to password')

    def set_user_fields(self):
        self.instance.set_password(self.cleaned_data.get('password'))
        self.instance.is_active = False


    class Meta:
        model = User
        fields = ['username', 'email']
