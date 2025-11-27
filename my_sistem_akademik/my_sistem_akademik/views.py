from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # cek group
            if user.groups.filter(name="admin").exists():
                return redirect("admin_home")

            elif user.groups.filter(name="guru").exists():
                return redirect("guru_dashboard")

            elif user.groups.filter(name="siswa").exists():
                return redirect("siswa_list")

            else:
                return render(request, "login.html", {"error": "User tidak punya role!"})

        else:
            return render(request, "login.html", {"error": "Username atau password salah!"})

    return render(request, "login.html")
