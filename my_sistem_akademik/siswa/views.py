from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Siswa, SPP
from .forms import SiswaForm

# ==========================================
# 1. HALAMAN KHUSUS SISWA (DASHBOARD)
# ==========================================
@login_required(login_url='/login/')
def siswa_dashboard(request):
    """Dashboard siswa dengan profil dan data pembayaran"""
    
    # PERBAIKAN: Gunakan relasi OneToOne (lebih aman daripada query manual)
    try:
        siswa = request.user.siswa  
    except AttributeError:
        # Jika user login tapi bukan siswa (misal Admin), set None
        siswa = None
    
    # Ambil data SPP
    spp_data = siswa.spp_siswa.all().order_by('-tahun', '-bulan') if siswa else []
    
    # Hitung ringkasan SPP
    spp_summary = {
        'total_tunggakan': 0,
        'bulan_belum_bayar': [],
        'spp_lunas': 0,
        'spp_belum': 0,
    }
    
    if siswa:
        for spp in spp_data:
            if spp.status == 'belum':
                spp_summary['total_tunggakan'] += float(spp.nominal)
                spp_summary['bulan_belum_bayar'].append(f"{spp.bulan}/{spp.tahun}")
                spp_summary['spp_belum'] += 1
            else:
                spp_summary['spp_lunas'] += 1
    
    context = {
        'siswa': siswa,
        'spp_data': spp_data,
        'spp_summary': spp_summary,
        # Tambahkan info user agar bisa menyapa "Halo, Nama"
        'user': request.user 
    }
    return render(request, "siswa_app/dashboard.html", context)


# ==========================================
# 2. HALAMAN KHUSUS ADMIN / GURU (CRUD)
# ==========================================

# Sebaiknya tambahkan login_required agar siswa/tamu tidak bisa akses halaman ini
@login_required(login_url='/login/') 
def siswa_list(request):
    data = Siswa.objects.all()
    return render(request, "siswa_app/list.html", {"siswa": data})

@login_required(login_url='/login/')
def siswa_tambah(request):
    form = SiswaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("siswa_list")
    
    return render(request, "siswa_app/form.html", {
        "title": "Tambah Siswa",
        "form": form,
    })

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
def siswa_detail(request, nis):
    siswa = get_object_or_404(Siswa, nis=nis)
    return render(request, "siswa_app/detail.html", {"siswa": siswa})

@login_required(login_url='/login/')
def siswa_hapus(request, nis):
    siswa = get_object_or_404(Siswa, nis=nis)
    if request.method == "POST":
        siswa.delete()
        return redirect("siswa_list")
    return render(request, "siswa_app/confirm_delete.html", {"siswa": siswa})