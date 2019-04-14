
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.html import strip_tags
from django.template.loader import render_to_string

from members.models import VerificationCode

import re
import hashlib
import random
from datetime import datetime, timedelta

class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_('Username'), max_length=30,
                               widget=forms.TextInput(attrs={
                                   'name': 'username',
                                   'placeholder': _('Username'),
                                   'required': True,
                                   'autofocus': True,
                                   'class': 'form-control'}))

    password = forms.CharField(label=_('Password'), max_length=30,
                               widget=forms.PasswordInput(attrs={
                                   'name': 'password',
                                   'placeholder': _('Password'),
                                   'class': 'form-control'}))


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Username', max_length=30,
                               widget=forms.TextInput(attrs={
                                   'name': 'username',
                                   'placeholder': _("Only alphabets and digits are permitted"),
                                   'required': True,
                                   'autofocus': True,
                                   'class': 'form-control'}))

    first_name = forms.CharField(label='First Name', max_length=30,
                                 widget=forms.TextInput(attrs={
                                     'name': 'first_name',
                                     'placeholder': 'First Name',
                                     'class': 'form-control'}))

    last_name = forms.CharField(label='Last Name', max_length=30,
                                widget=forms.TextInput(attrs={
                                    'name': 'last_name',
                                    'placeholder': 'Last Name',
                                    'class': 'form-control'}))

    email = forms.EmailField(label='Email', max_length=254,
                             widget=forms.TextInput(attrs={
                                 'name': 'email',
                                 'placeholder': 'Email',
                                 'class': 'form-control',}),
                             required=True)

    password1 = forms.CharField(label='Password', max_length=30,
                                widget=forms.PasswordInput(attrs={
                                    'name': 'password1',
                                    'placeholder': 'Password',
                                    'class': 'form-control'}))

    password2 = forms.CharField(label='Password', max_length=30,
                                widget=forms.PasswordInput(attrs={
                                    'name': 'password2',
                                    'placeholder': 'Confirm Password',
                                    'class': 'form-control'}))

    # def __init__(self, *args, **kwargs):
    #     self.fields['username'].error_messages = {"Invalid": _("The username is invalid")}

    # it's just model form.
    # https: // docs.djangoproject.com / en / 2.1 / topics / forms / modelforms /
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    # https: // docs.djangoproject.com / en / 2.1 / topics / forms / modelforms /
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_active = False
        if commit:
            user.save()
            # Generate the verification code object
            auth_code = self.gen_auth_code(user)
            # Send an email to the unauthenticated user
            # send_verification_email
            kwargs = {"username":user.username
                    ,"useremail":user.email
                    ,"auth_code":auth_code}
            self.send_verification_email(**kwargs)
        return user

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.fullmatch("^[a-zA-Z0-9]+$", username):
            raise forms.ValidationError(_("The username should contain only alphabets and digits"))
        if User.objects.filter(username__contains=username):
            raise forms.ValidationError(_("The username has been registered. Try another one."))
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        # Comment due to test
        # if User.objects.filter(email__contains = email):
        #     raise forms.ValidationError(_("The email has been registered"))
        return email

    def gen_auth_code(self, user):
        verification_code = VerificationCode()
        verification_code.user_fk = user
        salt = hashlib.sha256(str(random.random()).encode()).hexdigest()[:10]
        unique_hash = user.email
        # Incorrect. hashlib.sha256 returns an object which should be a value.
        verification_code.auth_code = hashlib.sha256((salt + unique_hash).encode()).hexdigest()[:32]
        verification_code.expiry_date = datetime.utcnow() + timedelta(days=3)
        verification_code.save()
        return verification_code.auth_code

    def send_verification_email(self, *args, **kwargs):
        username = kwargs['username']
        user_email = kwargs['useremail']
        auth_code = kwargs['auth_code']
        subject = "Welcome to Yuan's Shopping Mall, " + username
        ctx = {"username": username, "auth_code": auth_code}
        from_email = "YuanShoppingMall@gmail.com"
        to_email = user_email    # for testing
        html_message = render_to_string(template_name="members/verification_email.html", context=ctx)
        plain_msg = strip_tags(html_message)
        # Create the email template.
        # Check the src code to understand this API clearly!!!
        send_mail(
            subject,
            message=plain_msg,
            from_email=from_email,
            recipient_list=[to_email],
            html_message=html_message   # PEP 128...
        )
