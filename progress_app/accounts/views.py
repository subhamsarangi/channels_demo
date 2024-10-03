from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Profile


@login_required
def profile_view(request):
    try:
        profile = get_object_or_404(Profile, user=request.user)
        return render(request, "accounts/profile.html", {"profile": profile})
    except:
        return render(request, "accounts/profile.html", {"profile": None})
