from django.urls import path
from .views import login,register,dashboard,add_task,my_profile

urlpatterns = [
    path('login/',login,name='login'),
    path('register/',register,name='register'),
    path('task/',add_task,name='task'),
    path('dashboard/',dashboard,name='dashboard'),
    path('my_profile',my_profile,name='my_profile')
]

