from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView

from accounts.models import UserProfile


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


class UserprofileList(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'accounts/userprofile/userprofile-list.html'

    def get_queryset(self):
        nome = self.request.GET.get('q')
        if nome:
            object_list = self.model.objects.filter(nome__icontains=nome)
        else:
            object_list = self.model.objects.all()

        paginator = Paginator(object_list, 9)  # Show 9 contas per page

        page = self.request.GET.get('page')
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queryset = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            queryset = paginator.page(paginator.num_pages)

        # return object_list
        return queryset


class UserprofileDetalhe(SuccessMessageMixin, LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'accounts/userprofile/userprofile_detail.html'


class UserprofileUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'accounts/userprofile/userprofile_form.html'
    fields = '__all__'
    success_message = '%(nome) alterado com sucesso!'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.nome,
        )


def userprofile_delete(request, id=None):
    obj = get_object_or_404(UserProfile, id=id)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Registro apagado com sucesso!')
        return redirect('acc:userprofile-list')

    context = {
        'object': obj
    }

    return render(request, 'ctb/confirm_delete.html', context)
