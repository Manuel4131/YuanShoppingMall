from django.conf.urls import url
from django.contrib.auth import views as auth_views

from members import views as views
from members.forms import LoginForm

# members/
urlpatterns = [
    url(r'^profile/(?P<pk>\d+)/$', views.member_profile_view, name='profile'),
    # Not confirm this function
    url(r'^login/$', auth_views.login, {'template_name': 'members/login.html',
    'authentication_form': LoginForm}, name='login'),
    url(r'^register/$', views.member_registration_view, name='registration'),
    url(r'^registration/success/$', views.success_message_view, name="success"),
	url(r'^activate_account/(?P<auth_code>\w+)/$', views.validation_code_view, name='activate'),
	# url(r'^unsubscribe/$',)
	# url(r'^change_password/$', auth_views.password_change, name='change_psw') needs a fresh tmplt
]
