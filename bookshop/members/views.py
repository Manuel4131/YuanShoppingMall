from django.views.generic import DetailView, CreateView, TemplateView
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from members.forms import RegistrationForm
from members.models import VerificationCode

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'members/profile.html'

    def get_object(self, *args, **kwargs):
        current_user = self.request.user
        user = super(ProfileView, self).get_object(*args, **kwargs)

        if current_user.is_superuser or current_user.is_staff or current_user == user:
            return user

        raise PermissionDenied


class RegistrationView(CreateView):
    form_class = RegistrationForm
    model = User
    template_name = 'members/registration.html'

    def get_success_url(self):
        return reverse('members:success')


class SuccessMessageView(TemplateView):
    template_name = 'members/registration_success.html'


class ValidateCode(TemplateView):
    template_name = 'members/registration_success.html'


# Hurry UP!!! April 10
class ValidateActivationCode(TemplateView):
    # Create a new template and extract
    # these two tempaltes to base template

    def get_context_data(self, **kwargs):
        auth_code = self.kwargs.get('auth_code') # The dict which passed to the as_view method
                                                 # will be class attr
        try:
            auth_code_obj = VerificationCode.objects.get(auth_code=auth_code)
            auth_code_obj.delete()
            print("Successfully validate")      # Change it to log method
        except VerificationCode.DoesNotExist as e:
            raise Http404("Authentication code does not exist")

member_profile_view = ProfileView.as_view()
member_registration_view = RegistrationView.as_view()
success_message_view = SuccessMessageView.as_view()
validation_code_view = ValidateActivationCode.as_view()
