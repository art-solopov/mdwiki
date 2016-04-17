from django.views.generic.edit import FormView

from .forms import UserRegisterForm

class UserRegistration(FormView):

    """User registration view"""

    template_name = 'common/registration.html'
    success_url = '/'
    form_class = UserRegisterForm

    def form_valid(self, form):
        form.set_user_fields()
        form.save()
        return super().form_valid(form)
