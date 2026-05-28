from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


# =========================
# USER REGISTRATION VIEW
# =========================
def register(request):
    # Handle form submission (POST request)
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        # Create new user in database
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Automatically log the user in after registration
        login(request, user)

        # Redirect to home page after successful registration
        return redirect("home")

    # If GET request, show registration page
    return render(request, "accounts/register.html")


# =========================
# USER LOGIN VIEW
# =========================
def login_view(request):
    # Handle login form submission
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Authenticate user credentials
        user = authenticate(request, username=username, password=password)

        # If authentication successful
        if user is not None:
            login(request, user)
            return redirect("home")

        # If authentication fails
        else:
            messages.error(request, "Invalid credentials")

    # Show login page for GET request or failed login
    return render(request, "accounts/login.html")


# =========================
# USER LOGOUT VIEW
# =========================
def logout_view(request):
    # Log user out and clear session
    logout(request)

    # Redirect to login page after logout
    return redirect("login")