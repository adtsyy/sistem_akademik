from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Siswa
from .forms import SiswaForm

from laporan.models import SPP
from admin_app.models import Jadwal as AdminJadwal
from guru.models import Nilai as GuruNilai
from guru.models import Absen


# ==========================================================
# 1. DASHBOARD KHUSUS SISWA
# ==========================================================
@login_required(login_url='/login/')
def siswa_dashboard(request):

    # Ambil siswa dari user login
    siswa = getattr(request.user, "siswa", None)

    if not siswa:
        return render(request, "siswa_app/dashboard.html", {
            "error": "Akun ini belum terhubung sebagai siswa."
        })

    # DATA SPP
    spp_data = siswa.spp_siswa.all().order_by('bulan')

    total_tunggakan = 0
    spp_lunas = 0
    spp_belum = 0
    bulan_belum_bayar = []

    for spp in spp_data:
        if spp.status != "Lunas":
            kurang = spp.tagihan - spp.jumlah
            total_tunggakan += kurang
            bulan_belum_bayar.append(spp.get_bulan_display())
            spp_belum += 1
        else:
            spp_lunas += 1

    spp_summary = {
        "total_tunggakan": total_tunggakan,
        "bulan_belum_bayar": bulan_belum_bayar,
        "spp_lunas": spp_lunas,
        "spp_belum": spp_belum,
    }

    # JADWAL
    jadwal_kelas = siswa.jadwal

    return render(request, "siswa_app/dashboard.html", {
        "siswa": siswa,
        "spp_data": spp_data,
        "spp_summary": spp_summary,
        "jadwal_kelas": jadwal_kelas,
        "user": request.user,
    })


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
@login_required(login_url='/login/')
def jadwal_list(request):
    siswa = getattr(request.user, "siswa", None)

    if not siswa:
        return render(request, "siswa_app/jadwal_list.html", {
            "error": "Akun ini tidak terhubung sebagai siswa."
        })

    kelas_siswa = siswa.kelas
    jadwal_kelas = AdminJadwal.objects.filter(kelas=kelas_siswa).order_by('hari', 'jam_mulai')

    return render(request, 'siswa_app/jadwal_list.html', {
        'siswa': siswa,
        'jadwal_kelas': jadwal_kelas,
    })


# ==========================================================
# 8. NILAI SISWA
# ==========================================================
@login_required(login_url='/login/')
def nilai_siswa(request):
    siswa = getattr(request.user, "siswa", None)

    if not siswa:
        return render(request, "siswa_app/nilai.html", {
            "error": "Akun ini tidak terhubung sebagai siswa."
        })

    nilai_list = GuruNilai.objects.filter(siswa=siswa).select_related('jadwal')

    return render(request, 'siswa_app/nilai.html', {
        'nilai_list': nilai_list,
        'siswa': siswa
    })


# ==========================================================
# 9. ABSEN SISWA
# ==========================================================
@login_required(login_url='/login/')
def absen_siswa(request):
    siswa = getattr(request.user, "siswa", None)

    if not siswa:
        return render(request, "siswa_app/absen_siswa.html", {
            "error": "Akun ini tidak terhubung sebagai siswa."
        })

    absen_list = Absen.objects.filter(siswa=siswa).select_related('jadwal')

    return render(request, 'siswa_app/absen_siswa.html', {
        'absen_list': absen_list,
        'siswa': siswa
    })
