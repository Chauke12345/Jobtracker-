from django.urls import path
from . import views
from .views import logout_view

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]