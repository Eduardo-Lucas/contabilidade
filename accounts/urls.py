from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.core.urlresolvers import reverse_lazy

from accounts import views
from accounts.views import UserprofileList, UserprofileDetalhe, UserprofileUpdate, userprofile_delete

app_name = 'accounts'

urlpatterns = [
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^password-change', auth_views.PasswordChangeView.as_view(), name='password_change'),
    url(r'^reset-password/$', auth_views.PasswordResetView.as_view(
        success_url=reverse_lazy('password_reset_done'),
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/email/password_reset_subject.txt'
    ), name='password_reset'),
    url(r'^reset-password/done/$', auth_views.PasswordResetDoneView, name='password_reset_done'),

    url(r'^userprofile-list/$', UserprofileList.as_view(), name='userprofile-list'),
    url(r'^userprofile-list/(?P<pk>[0-9]+)/$', UserprofileDetalhe.as_view(), name='userprofile-detail'),
    url(r'^userprofile/(?P<pk>[0-9]+)/edit/$', UserprofileUpdate.as_view(), name='userprofile-edit'),
    url(r'^userprofile/(?P<id>[0-9]+)/delete/$', userprofile_delete, name='userprofile-delete'),

]

"""
        url(r'^login/', login_view, name='login'),
        url(r'^register/', register_view, name='register'),
        url(r'^logout/', logout_view, name='logout'),
"""
