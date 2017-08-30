from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

from django.shortcuts import render, redirect

from django.views.generic import ListView, DetailView, UpdateView
from accounts.models import UserProfile
from .forms import UserLoginForm


# Create your views here.


def login_view(request):
    title = 'Login'
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("/ctb")

    context = {
        'form': form,
        'title': title
    }
    return render(request, "accounts/form.html", context)


class ProfileList(ListView):
    model = UserProfile
    template_name = 'accounts/profile-index.html'


class ProfileDetalhe(DetailView):
    model = UserProfile
    template_name = 'accounts/profile-detail.html'


class ProfileUpdate(UpdateView):
    model = UserProfile
    exclude = ['usuario']
    fields = '__all__'
    template_name = 'accounts/userprofile_form.html'

"""
def register_view(request):
    title = "Registro"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect("/ctb")

    context = {
        'form': form,
        'title': title
    }
    return render(request, "accounts/form.html", context)


def logout_view(request):
    logout(request)
    return redirect("/acc/login")
"""
