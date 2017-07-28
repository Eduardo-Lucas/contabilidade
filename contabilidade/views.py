from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home_principal(request):
    return render(request, "index.html", {})
