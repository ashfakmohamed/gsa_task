# app>views.py

from django.shortcuts import render, redirect
from .models import User, Task
from django.contrib import messages
from datetime import datetime
from geopy.geocoders import ArcGIS

def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        password = request.POST.get('password')
        address = request.POST.get('address')
        geolocator = ArcGIS()
        location = geolocator.geocode(address)
        latitude = location.latitude
        longitude = location.longitude

        user = User(name=name, email=email, mobile_number=mobile_number, password=password, address=address, latitude=latitude, longitude=longitude)
        user.save()
        return redirect('login')
    return render(request, 'register.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        request.session['email'] = email

        user = User.objects.filter(email=email).first()
        if not user:
            messages.error(request, 'User not Found!')
            return redirect('login')
        elif password != user.password:
            messages.error(request, "Password invalid!")
            return redirect('login')
        else:
            return redirect('dashboard')
    return render(request, 'login.html')

def dashboard(request):
    tasks = Task.objects.all()
    return render(request, 'dashboard.html', {'tasks': tasks})

def add_task(request):
    if request.method == "POST":
        name = request.POST.get('name')
        date_time = request.POST.get('date_time')
        assigned_to = request.POST.get('assigned_to')
        address = request.POST.get('address')
        
        geolocator = ArcGIS()
        location = geolocator.geocode(address)
        latitude = location.latitude
        longitude = location.longitude

        date, time = date_time.split('T')
        status = None

        current_date = datetime.now().date()
        input_date = datetime.strptime(date, "%Y-%m-%d").date()

        if input_date == current_date or current_date < input_date:
            status = 'Pending'
        elif input_date < current_date:
            status = 'Completed'

        task = Task(name=name, date=date, time=time, assigned_to=assigned_to, status=status, latitude=latitude, longitude=longitude)
        task.save()
        return redirect('dashboard')
    return render(request, 'task.html')

def my_profile(request):
    user = User.objects.filter(email=request.session['email']).first()
    return render(request, 'my_profile.html', {'value': user})