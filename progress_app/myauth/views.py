from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from .forms import RegistrationForm, LoginForm
from accounts.models import Profile


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            Profile.objects.create(user=user)
            return redirect("myauth:login")
    else:
        form = RegistrationForm()
    return render(request, "auth/register.html", {"form": form})


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = "auth/login.html"
