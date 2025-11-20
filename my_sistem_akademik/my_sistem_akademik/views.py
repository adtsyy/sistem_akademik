from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autentikasi user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 🔁 Redirect sementara: semua user kembali ke halaman login
            # Nanti akan diganti dengan redirect ke dashboard masing-masing
            messages.success(request, f"Login berhasil! Selamat datang, {username}.")
            return redirect('login')  # redirect ke URL dengan name='login'

        else:
            messages.error(request, "Username atau password salah.")

    return render(request, 'login.html')