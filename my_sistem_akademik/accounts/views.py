from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # cek role
            role = UserProfile.objects.get(user=user).role

            if role == "admin":
                return redirect("admin_dashboard")
            elif role == "guru":
                return redirect("guru_dashboard")
            elif role == "siswa":
                return redirect("siswa_dashboard")

        messages.error(request, "Username atau password salah")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")
