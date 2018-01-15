from django.conf.urls.defaults import *

from project.forms import RegistrationForm, RegistrationFormPartner

urlpatterns = patterns('project.views',
	url(r'^accounts/profile/$', 'profile_views', name='profile_url'),
	url(r'^accounts/change-password/$', 'profile_change_password', name='profile_change_password_url'),
	
	url(r'^accounts/profile/forum/thread/$', 'profile_thread', name='profile_thread_url'),
	url(r'^accounts/profile/forum/post/$', 'profile_post', name='profile_post_url'),
)

urlpatterns += patterns('',
	url(r'^accounts/register/$', 'registration.views.register', {'form_class':RegistrationForm}, name='registration_register'),
	url(r'^accounts/register-partner/$', 'registration.views.register', {'form_class':RegistrationFormPartner, 'success_url': '/accounts/register-partner/complete/'}, name='registration_register_partner'),
	url(r'^accounts/activate-partner/(?P<activation_key>\w+)/$', 'project.views.activate_partner',  name='registration_activate_partner'),
)