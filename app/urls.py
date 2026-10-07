from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("tasks/new/", views.add_task, name="task"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.my_profile, name="my_profile"),
]
