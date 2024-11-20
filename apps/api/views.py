from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from ninja import Router, NinjaAPI

from .models import Profile

api_api = NinjaAPI(urls_namespace="api")
api_router = Router()
api_api.add_router("", api_router)


@api_router.get("/profile")
@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, "api/profile.html", {"profile": profile})
