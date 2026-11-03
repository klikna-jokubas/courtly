from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("court_list")

    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {
        "form": form
    })

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("court_list")
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


@require_POST
def user_logout(request):
    logout(request)
    return redirect("court_list")