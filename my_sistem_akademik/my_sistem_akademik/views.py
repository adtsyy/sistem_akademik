from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# =========================
# VIEW LOGIN
# =========================
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autentikasi user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Login berhasil! Selamat datang, {username}.")

            # Redirect berdasarkan username
            if 'guru' in username.lower():
                return redirect('guru_dashboard')  # ← URL name dari guru/urls.py
            elif 'siswa' in username.lower():
                messages.info(request, "Halaman siswa belum tersedia.")
                return redirect('login')
            elif 'admin' in username.lower():
                messages.info(request, "Halaman admin belum tersedia.")
                return redirect('login')
            else:
                messages.error(request, "Peran pengguna tidak dikenali.")
                return redirect('login')

        else:
            messages.error(request, "Username atau password salah.")

    # Jika method GET atau login gagal, tampilkan halaman login
    return render(request, 'login.html')


# =========================
# VIEW DASHBOARD GURU (untuk referensi)
# =========================
@login_required
def dashboard_guru(request):
    return render(request, 'guru/dashboard.html')


# =========================
# VIEW LOGOUT
# =========================
def logout_view(request):
    logout(request)
    return redirect('login')