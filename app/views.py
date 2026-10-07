from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_POST
from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from geopy.geocoders import ArcGIS

from .forms import LoginForm, RegistrationForm, TaskForm
from .models import Profile, Task


def geocode_address(address):
    if not address:
        return None, None
    try:
        location = ArcGIS(timeout=5).geocode(address, timeout=5)
    except (GeocoderServiceError, GeocoderTimedOut, ValueError):
        return None, None
    if location is None:
        return None, None
    return location.latitude, location.longitude


@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        latitude, longitude = geocode_address(form.cleaned_data["address"])
        with transaction.atomic():
            user = User.objects.create_user(
                username=form.cleaned_data["email"],
                email=form.cleaned_data["email"],
                first_name=form.cleaned_data["name"],
                password=form.cleaned_data["password1"],
            )
            Profile.objects.create(
                user=user,
                mobile_number=form.cleaned_data["mobile_number"],
                address=form.cleaned_data["address"],
                latitude=latitude,
                longitude=longitude,
            )
        auth_login(request, user)
        messages.success(request, "Your account was created successfully.")
        return redirect("dashboard")

    return render(request, "register.html", {"form": form})


@require_http_methods(["GET", "POST"])
def login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"].strip().lower()
        user = authenticate(
            request,
            username=email,
            password=form.cleaned_data["password"],
        )
        if user is not None:
            auth_login(request, user)
            return redirect("dashboard")
        messages.error(request, "Invalid email or password.")

    return render(request, "login.html", {"form": form})


@login_required
@require_POST
def logout(request):
    auth_logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    today = timezone.localdate()
    Task.objects.filter(
        owner=request.user,
        date__lt=today,
        status=Task.Status.PENDING,
    ).update(status=Task.Status.COMPLETED)
    tasks = Task.objects.filter(owner=request.user)
    return render(request, "dashboard.html", {"tasks": tasks})


@login_required
@require_http_methods(["GET", "POST"])
def add_task(request):
    form = TaskForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        scheduled_at = form.cleaned_data["date_time"]
        latitude, longitude = geocode_address(form.cleaned_data["address"])
        status = (
            Task.Status.COMPLETED
            if scheduled_at.date() < timezone.localdate()
            else Task.Status.PENDING
        )
        Task.objects.create(
            owner=request.user,
            name=form.cleaned_data["name"],
            date=scheduled_at.date(),
            time=scheduled_at.time(),
            assigned_to=form.cleaned_data["assigned_to"],
            address=form.cleaned_data["address"],
            status=status,
            latitude=latitude,
            longitude=longitude,
        )
        messages.success(request, "Task added successfully.")
        return redirect("dashboard")

    return render(request, "task.html", {"form": form})


@login_required
def my_profile(request):
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={"mobile_number": "", "address": ""},
    )
    return render(request, "my_profile.html", {"profile": profile})
