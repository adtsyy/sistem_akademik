from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# =========================
# VIEW REDIRECT KE LOGIN
# =========================
def redirect_to_login(request):
    """Redirect user ke login jika belum authenticated, atau ke dashboard jika sudah"""
    if request.user.is_authenticated:
        # Jika user sudah login, redirect ke dashboard sesuai role
        username = request.user.username.lower()
        if 'guru' in username:
            return redirect('guru_dashboard')
        elif 'admin' in username:
            return redirect('index')
        elif 'siswa' in username:
            return redirect('siswa_dashboard')
        else:
            return redirect('login')
    return redirect('login')

# =========================
# VIEW LOGIN
# =========================
def login_view(request):
    if request.user.is_authenticated:
        # Jika sudah login, redirect ke dashboard
        return redirect_to_login(request)
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, "Username dan password harus diisi.")
            return render(request, 'login.html')

        # Autentikasi user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f"Login berhasil! Selamat datang, {username}.")

                # Redirect berdasarkan username
                username_lower = username.lower()
                if 'guru' in username_lower:
                    return redirect('guru_dashboard')
                elif 'siswa' in username_lower:
                    return redirect('siswa_dashboard')
                elif 'admin' in username_lower:
                    return redirect('index')
                else:
                    return redirect('guru_dashboard')  # Default redirect
            else:
                messages.error(request, "Akun Anda tidak aktif. Hubungi administrator.")
        else:
            messages.error(request, "Username atau password salah.")

    # Jika method GET atau login gagal, tampilkan halaman login
    return render(request, 'login.html')

# =========================
# VIEW LOGOUT
# =========================
def logout_view(request):
    logout(request)
    messages.success(request, "Logout berhasil. Sampai jumpa!")
    return redirect('login')