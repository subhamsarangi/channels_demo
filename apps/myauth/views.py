from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib import messages

from apps.api.models import Profile
from .forms import RegistrationForm, LoginForm


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

    def get(self, request, *args, **kwargs):
        # Check if redirected from another view
        next_url = request.GET.get("next")
        if next_url:
            messages.info(request, "You need to log in to access this page.")
        return super().get(request, *args, **kwargs)
