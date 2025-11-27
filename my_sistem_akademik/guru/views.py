from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_guru(request):
    return render(request, 'guru/dashboard.html')

# 📚 Data jadwal sementara (untuk testing)
# Format: { 'username_guru': ['Kelas A', 'Kelas B', ...] }
JADWAL_GURU = {
    'guru_math': ['X IPA 1', 'X IPA 2', 'XI MIPA 1'],
    'guru_biology': ['X IPA 3', 'XI MIPA 2', 'XII MIPA 1'],
}

@login_required
def dashboard_guru(request):
    return render(request, 'guru/dashboard.html')

@login_required
def absen_siswa(request):
    username = request.user.username
    kelas_list = JADWAL_GURU.get(username, [])
    context = {
        'kelas_list': kelas_list,
        'nama_guru': username,
    }
    return render(request, 'guru/absen.html', context)

@login_required
def input_nilai(request):
    username = request.user.username
    kelas_list = JADWAL_GURU.get(username, [])
    context = {
        'kelas_list': kelas_list,
        'nama_guru': username,
    }
    return render(request, 'guru/input_nilai.html', context)