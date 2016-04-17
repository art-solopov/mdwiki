from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^accounts/register', views.UserRegistration.as_view(),
        name='register'),
]
