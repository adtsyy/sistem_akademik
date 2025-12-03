from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from datetime import datetime
from admin_app.models import Pegawai, Jadwal
from siswa.models import Siswa
from .models import Absen, Nilai


def get_guru_from_user(user):
    """Ambil data Pegawai dari User yang login"""
    try:
        # Cara paling andal: gunakan related_name 'pegawai' dari OneToOneField
        return user.pegawai
    except Pegawai.DoesNotExist:
        return None


@login_required
def dashboard_guru(request):
    """Dashboard utama guru"""
    pegawai = get_guru_from_user(request.user)
    context = {
        'pegawai': pegawai,
        'nama_guru': request.user.first_name or request.user.username,
    }
    return render(request, 'guru/dashboard.html', context)


@login_required
def jadwal_guru(request):
    """Tampilkan jadwal guru dari database"""
    pegawai = get_guru_from_user(request.user)
    
    if not pegawai:
        context = {'jadwal_list': [], 'pegawai': None}
    else:
        jadwal_list = Jadwal.objects.filter(pegawai=pegawai).order_by('hari', 'jam_mulai')
        context = {
            'jadwal_list': jadwal_list,
            'pegawai': pegawai,
        }
    
    return render(request, 'guru/jadwal_guru.html', context)


@login_required
def absen_siswa(request):
    """Halaman absen siswa dengan filter"""
    pegawai = get_guru_from_user(request.user)
    
    # Ambil jadwal guru
    jadwal_list = []
    kelas_list = []
    mapel_list = []
    hari_list = []
    siswa_list = []
    
    if pegawai:
        jadwal_list = Jadwal.objects.filter(pegawai=pegawai)
        kelas_list = list(set(Siswa.objects.values_list('kelas', flat=True)))
        mapel_list = list(set(jadwal_list.values_list('mata_pelajaran', flat=True)))
        hari_list = list(set(jadwal_list.values_list('hari', flat=True)))
    
    # Filter berdasarkan request
    selected_jadwal = request.GET.get('jadwal')
    selected_kelas = request.GET.get('kelas', '')  # Ambil filter kelas
    search_siswa = request.GET.get('search', '').strip()
    
    siswa_list = Siswa.objects.all()
    
    # Terapkan filter kelas jika ada
    if selected_kelas:
        siswa_list = siswa_list.filter(kelas=selected_kelas)
    
    # Terapkan filter pencarian
    if search_siswa:
        siswa_list = siswa_list.filter(
            Q(nama__icontains=search_siswa) | Q(nis__icontains=search_siswa)
        )
    
    # Handle POST (submit absen)
    if request.method == 'POST':
        siswa_id = request.POST.get('siswa_id')
        jadwal_id = request.POST.get('jadwal_id')
        status = request.POST.get('status')
        tanggal = request.POST.get('tanggal', datetime.now().date())
        keterangan = request.POST.get('keterangan', '')
        
        try:
            siswa = Siswa.objects.get(nis=siswa_id)
            jadwal = Jadwal.objects.get(id=jadwal_id, pegawai=pegawai)
            
            absen, created = Absen.objects.update_or_create(
                siswa=siswa,
                jadwal=jadwal,
                tanggal=tanggal,
                defaults={
                    'pegawai': pegawai,
                    'status': status,
                    'keterangan': keterangan,
                }
            )
            return JsonResponse({'success': True, 'message': 'Absen berhasil disimpan'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    context = {
        'jadwal_list': jadwal_list,
        'kelas_list': sorted(kelas_list), # Gunakan daftar kelas lengkap untuk dropdown
        'mapel_list': sorted(mapel_list),
        'hari_list': sorted(hari_list),
        'siswa_list': siswa_list[:20],  # Limit awal
        'pegawai': pegawai,
        'selected_kelas': selected_kelas, # Kirim filter aktif ke template
        'selected_jadwal': selected_jadwal,
        'search_siswa': search_siswa,
    }
    
    return render(request, 'guru/absen.html', context)


@login_required
def input_nilai(request):
    """Halaman input nilai siswa dengan filter mirip absen"""
    pegawai = get_guru_from_user(request.user)
    
    # Ambil jadwal guru
    jadwal_list = []
    kelas_list = []
    mapel_list = []
    hari_list = []
    siswa_list = []
    
    if pegawai:
        jadwal_list = Jadwal.objects.filter(pegawai=pegawai)
        kelas_list = list(set(Siswa.objects.values_list('kelas', flat=True)))
        mapel_list = list(set(jadwal_list.values_list('mata_pelajaran', flat=True)))
        hari_list = list(set(jadwal_list.values_list('hari', flat=True)))
    
    # Filter berdasarkan request
    selected_jadwal = request.GET.get('jadwal')
    selected_kelas = request.GET.get('kelas', '') # Ambil filter kelas
    search_siswa = request.GET.get('search', '').strip()
    
    siswa_list = Siswa.objects.all()
    
    # Terapkan filter kelas jika ada
    if selected_kelas:
        siswa_list = siswa_list.filter(kelas=selected_kelas)
        
    # Terapkan filter pencarian
    if search_siswa:
        siswa_list = siswa_list.filter(
            Q(nama__icontains=search_siswa) | Q(nis__icontains=search_siswa)
        )
    
    # Handle POST (submit nilai)
    if request.method == 'POST':
        siswa_id = request.POST.get('siswa_id')
        jadwal_id = request.POST.get('jadwal_id')
        nilai = request.POST.get('nilai')
        tanggal = request.POST.get('tanggal', datetime.now().date())
        keterangan = request.POST.get('keterangan', '')
        
        try:
            nilai_float = float(nilai)
            if not (0 <= nilai_float <= 100):
                return JsonResponse({'success': False, 'message': 'Nilai harus antara 0-100'})
            
            siswa = Siswa.objects.get(nis=siswa_id)
            jadwal = Jadwal.objects.get(id=jadwal_id, pegawai=pegawai)
            
            nilai_obj, created = Nilai.objects.update_or_create(
                siswa=siswa,
                jadwal=jadwal,
                tanggal=tanggal,
                defaults={
                    'pegawai': pegawai,
                    'nilai': nilai_float,
                    'keterangan': keterangan,
                }
            )
            return JsonResponse({'success': True, 'message': 'Nilai berhasil disimpan'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    context = {
        'jadwal_list': jadwal_list,
        'kelas_list': sorted(kelas_list), # Gunakan daftar kelas lengkap untuk dropdown
        'mapel_list': sorted(mapel_list),
        'hari_list': sorted(hari_list),
        'siswa_list': siswa_list[:20],  # Limit awal
        'pegawai': pegawai,
        'selected_kelas': selected_kelas, # Kirim filter aktif ke template
        'selected_jadwal': selected_jadwal,
        'search_siswa': search_siswa,
    }
    
    return render(request, 'guru/input_nilai.html', context)