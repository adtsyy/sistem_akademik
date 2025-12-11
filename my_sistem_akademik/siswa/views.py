from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Siswa, SPP, Nilai
from .forms import SiswaForm

# Import Jadwal dari admin_app
from admin_app.models import Jadwal as AdminJadwal
from guru.models import Nilai as GuruNilai
from guru.models import Absen

# ==========================================================
# 1. DASHBOARD KHUSUS SISWA
# ==========================================================
@login_required(login_url='/login/')
def siswa_dashboard(request):

    # Ambil siswa berdasarkan user login
    siswa = getattr(request.user, "siswa", None)

    # Jika user bukan siswa
    if not siswa:
        return render(request, "siswa_app/dashboard.html", {
            "error": "Akun ini belum terhubung sebagai siswa."
        })

    # -------------------------------------------------------
    # DATA SPP
    # -------------------------------------------------------
    spp_data = siswa.spp_siswa.all().order_by('bulan')  # FIX: related_name spp_siswa

    spp_summary = {
        "total_tunggakan": 0,
        "bulan_belum_bayar": [],
        "spp_lunas": 0,
        "spp_belum": 0,
    }

    for spp in spp_data:
        if spp.status != "lunas":
            spp_summary["bulan_belum_bayar"].append(spp.bulan)
            spp_summary["spp_belum"] += 1
        else:
            spp_summary["spp_lunas"] += 1


    # -------------------------------------------------------
    # JADWAL SISWA
    # -------------------------------------------------------
    jadwal_kelas = siswa.jadwal

    # -------------------------------------------------------
    # KIRIM DATA KE TEMPLATE
    # -------------------------------------------------------
    context = {
        "siswa": siswa,
        "spp_data": spp_data,
        "spp_summary": spp_summary,
        "jadwal_kelas": jadwal_kelas,
        "user": request.user,
    }

    return render(request, "siswa_app/dashboard.html", context)



# ==========================================================
# 2. LIST SISWA
# ==========================================================

def siswa_list(request):
    data = Siswa.objects.all()
    return render(request, "siswa_app/list.html", {"siswa": data})


# ==========================================================
# 3. TAMBAH SISWA
# ==========================================================
def siswa_tambah(request):
    form = SiswaForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("siswa_list")

    return render(request, "siswa_app/form.html", {
        "title": "Tambah Siswa",
        "form": form,
    })


# ==========================================================
# 4. EDIT SISWA
# ==========================================================
def siswa_edit(request, nis):
    siswa = get_object_or_404(Siswa, nis=nis)
    form = SiswaForm(request.POST or None, instance=siswa)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("siswa_list")

    return render(request, "siswa_app/form.html", {
        "title": "Edit Siswa",
        "form": form,
        "siswa": siswa
    })


# ==========================================================
# 5. DETAIL SISWA
# ==========================================================
def siswa_detail(request, nis):
    siswa = get_object_or_404(Siswa, nis=nis)
    return render(request, "siswa_app/detail.html", {"siswa": siswa})


# ==========================================================
# 6. HAPUS SISWA
# ==========================================================
def siswa_hapus(request, nis):
    siswa = get_object_or_404(Siswa, nis=nis)

    if request.method == "POST":
        siswa.delete()
        return redirect("siswa_list")

    return render(request, "siswa_app/confirm_delete.html", {"siswa": siswa})


# ==========================================================
# 7. JADWAL SISWA
# ==========================================================
def jadwal_list(request):
    siswa = Siswa.objects.get(user=request.user)
    kelas_siswa = siswa.kelas

    jadwal_kelas = AdminJadwal.objects.filter(kelas=kelas_siswa).order_by('hari', 'jam_mulai')

    return render(request, 'siswa_app/jadwal_list.html', {
        'siswa': siswa,
        'jadwal_kelas': jadwal_kelas,
    })


# ==========================================================
# 8. NILAI SISWA (VIEW BARU IMPLEMENTASI)
# ==========================================================
@login_required(login_url='/login/')
def nilai_siswa(request):

    siswa = getattr(request.user, "siswa", None)
    if not siswa:
        return render(request, "siswa_app/nilai.html", {
            "error": "Akun ini tidak terhubung sebagai siswa."
        })

    # Ambil semua nilai siswa (berdasarkan model Nilai)
    nilai_list = siswa.nilai_siswa.select_related('mapel').all()

    return render(request, "siswa_app/nilai.html", {
        "siswa": siswa,
        "nilai_list": nilai_list,
    })

def nilai_siswa(request):
    siswa = request.user.siswa  # otomatis ambil data siswa dari user login
    nilai_list = GuruNilai.objects.filter(siswa=siswa).select_related('jadwal')

    return render(request, 'siswa_app/nilai.html', {
        'nilai_list': nilai_list
    })

def absen_siswa(request):
    siswa = request.user.siswa
    absen_list = Absen.objects.filter(siswa=siswa).select_related('jadwal')

    return render(request, 'siswa_app/absen_siswa.html', {
        'absen_list': absen_list
    })