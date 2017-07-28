from django.conf.urls import url
from .views import register_view, login_view, logout_view

app_name = 'accounts'

urlpatterns = [
    url(r'^register/', register_view, name='register'),
    url(r'^login', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),

]
