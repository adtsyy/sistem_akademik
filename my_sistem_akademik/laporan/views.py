from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Rapor, SPP, Gaji
from .forms import RaporForm, SPPForm, GajiForm
from siswa.models import Siswa
from django.db.models import Q
from django.db.models import Avg, Sum, Count
from .models import Rapor
from guru.models import Nilai, Absen 
import calendar

def home(request):
    return render(request, 'laporan/home.html')

# 1. LIST RAPOR (Tampilan Awal)
class RaporListView(ListView):
    model = Rapor
    template_name = 'laporan/rapor_list.html'
    context_object_name = 'rapor'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(siswa__nama__icontains=search)
        return queryset

# 2. LANGKAH 1: CARI SISWA
def tambah_rapor_step1(request):
    """Halaman pencarian siswa sebelum generate rapor"""
    search_query = request.GET.get('q', '')
    siswa_list = []

    if search_query:
        siswa_list = Siswa.objects.filter(
            Q(nama__icontains=search_query) | 
            Q(nis__icontains=search_query)
        )

    return render(request, 'laporan/rapor_search.html', {
        'siswa_list': siswa_list,
        'search_query': search_query
    })

# 3. LANGKAH 2: GENERATE & SIMPAN (LOGIC INTI)
def generate_rapor_siswa(request, id_siswa):
    # Ambil data siswa
    siswa = get_object_or_404(Siswa, pk=id_siswa)

    # Cek duplikasi (Opsional: 1 Siswa 1 Rapor)
    if Rapor.objects.filter(siswa=siswa).exists():
        messages.warning(request, f"Rapor untuk {siswa.nama} sudah ada!")
        return redirect('rapor_list')

    # --- HITUNG NILAI ---
    nilai_qs = Nilai.objects.filter(siswa=siswa).select_related('jadwal')
    
    data_mapel = {}
    total_nilai = 0
    jumlah_mapel = 0

    if nilai_qs.exists():
        # Grouping nilai per mata pelajaran
        temp_group = {}
        for obj in nilai_qs:
            mapel = obj.jadwal.mata_pelajaran
            if mapel not in temp_group:
                temp_group[mapel] = []
            temp_group[mapel].append(obj.nilai)
        
        # Hitung rata-rata per mapel
        for mapel, list_nilai in temp_group.items():
            avg_per_mapel = sum(list_nilai) / len(list_nilai)
            data_mapel[mapel] = round(avg_per_mapel, 2) # Simpan ke Dict JSON
            
            total_nilai += avg_per_mapel
            jumlah_mapel += 1
        
        rata_rata_akhir = round(total_nilai / jumlah_mapel, 2) if jumlah_mapel > 0 else 0
    else:
        rata_rata_akhir = 0

    # --- HITUNG ABSENSI  ---
    absen_sakit = Absen.objects.filter(siswa=siswa, status='sakit').count()
    absen_izin = Absen.objects.filter(siswa=siswa, status='izin').count()
    absen_alpa = Absen.objects.filter(siswa=siswa, status='alpa').count()
    
    # Masukkan info absen ke JSON juga agar tersimpan di rapor
    data_mapel['Absensi'] = {
        'Sakit': absen_sakit,
        'Izin': absen_izin,
        'Alpa': absen_alpa
    }

    # --- TENTUKAN PREDIKAT ---
    if rata_rata_akhir >= 90:
        predikat, ket = "A", "Sangat Baik"
    elif rata_rata_akhir >= 80:
        predikat, ket = "B", "Baik"
    elif rata_rata_akhir >= 70:
        predikat, ket = "C", "Cukup"
    else:
        predikat, ket = "D", "Kurang"

    # --- SIMPAN KE DATABASE ---
    Rapor.objects.create(
        siswa=siswa,            # Relasi Foreign Key
        nama=siswa.nama,        # Snapshot Nama
        kelas=siswa.kelas,      # Snapshot Kelas
        nilai_mapel=data_mapel, # Simpan hasil hitungan JSON
        rata_rata=rata_rata_akhir,
        predikat=predikat,
        keterangan=ket
    )

    messages.success(request, f"Sukses! Rapor {siswa.nama} berhasil dibuat.")
    return redirect('rapor_list')

class RaporUpdateView(UpdateView):
    model = Rapor
    template_name = 'laporan/rapor_form.html'
    # Field ini akan dirender oleh {{ form.rata_rata }}, {{ form.predikat }}, dll di template
    fields = ['rata_rata', 'predikat', 'keterangan', 'nilai_mapel', 'siswa'] 
    success_url = reverse_lazy('rapor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mengirim data tambahan untuk judul di atas form
        context['siswa_nama'] = self.object.siswa.nama
        context['siswa_kelas'] = self.object.kelas
        return context
    
# HAPUS RAPOR
class RaporDeleteView(DeleteView):
    model = Rapor
    template_name = 'laporan/rapor_confirm_delete.html'
    success_url = reverse_lazy('rapor_list')

# DETAIL RAPOR
class RaporDetailView(DetailView):
    model = Rapor
    template_name = 'laporan/rapor_detail.html'
    context_object_name = 'rapor'

# List SPP
def spp_list(request):
    # Ambil semua data
    spp = SPP.objects.select_related('siswa').all()
    keyword = request.GET.get('q')

    if keyword:
        spp = spp.filter(
            Q(siswa__nama__icontains=keyword) |  # Cari berdasarkan Nama
            Q(siswa__nis__icontains=keyword)     # ATAU Cari berdasarkan NIS
        )

    # Tambahkan bulan_nama ke setiap objek SPP dalam queryset
    for record in spp:
        record.bulan_nama = calendar.month_name[record.bulan]  # Menambahkan nama bulan

    return render(request, 'laporan/spp_list.html', {'spp': spp, 'keyword': keyword})

# Tambah SPP
def spp_tambah(request):
    siswa_list = Siswa.objects.all()

    if request.method == 'POST':
        data = request.POST.copy()
        
        siswa_id = request.POST.get('siswa') 
        data['siswa'] = siswa_id

        form = SPPForm(data)
        
        if form.is_valid():
            # 1. Jangan simpan ke database dulu (commit=False)
            spp_baru = form.save(commit=False)
            
            # 2. CEK: Apakah Siswa ini di Bulan ini sudah ada datanya?
            spp_lama = SPP.objects.filter(
                siswa=spp_baru.siswa, 
                bulan=spp_baru.bulan
            ).first()
            
            if spp_lama:
                spp_lama.jumlah += spp_baru.jumlah 
                spp_lama.tagihan = spp_baru.tagihan 
                spp_lama.save() 
            else:
                spp_baru.save()
            
            return redirect('spp_list')

        # Jika form error
        return render(request, 'laporan/spp_form.html', {
            'form': form,
            'siswa_list': siswa_list
        })

    # GET Request
    form = SPPForm()
    return render(request, 'laporan/spp_form.html', {
        'form': form,
        'siswa_list': siswa_list
    })

# Edit SPP
def spp_edit(request, id):
    spp = get_object_or_404(SPP, id=id)

    if request.method == 'POST':
        form = SPPForm(request.POST, instance=spp)
        if form.is_valid():

            spp = form.save(commit=False)
            siswa_id = request.POST.get("siswa")    
            spp.siswa_id = siswa_id                 

            spp.save()
            return redirect('spp_list')

    # GET → tampilkan form dengan data lama
    form = SPPForm(instance=spp)
    siswa_list = Siswa.objects.all()

    return render(request, 'laporan/spp_form.html', {
        'form': form,
        'siswa_list': siswa_list
    })

# HAPUS
def spp_hapus(request, id):
    spp = get_object_or_404(SPP, id=id)

    if request.method == "POST":
        spp.delete()
        return redirect('spp_list')

    # Kirim spp ke template untuk konfirmasi
    return render(request, 'laporan/spp_confirm_delete.html', {'object': spp})

def gaji_list(request):
    gaji = Gaji.objects.select_related('pegawai').all().order_by('-id')

    # Logika Pencarian
    keyword = request.GET.get('q')
    if keyword:
        gaji = gaji.filter(
            Q(pegawai__nama__icontains=keyword) |       # Cari Nama
            Q(pegawai__id_pegawai__icontains=keyword) | # Cari ID Pegawai
            Q(bulan__icontains=keyword)                 # Cari Bulan
        )

    return render(request, "laporan/gaji_list.html", {"gaji": gaji, "keyword": keyword})

# Tambah Gaji
def gaji_tambah(request):
    if request.method == "POST":
        form = GajiForm(request.POST)
        if form.is_valid():
            gaji_baru = form.save(commit=False)
            
            # CEK APAKAH SUDAH ADA GAJI BULAN INI UNTUK PEGAWAI INI?
            cek_ganda = Gaji.objects.filter(
                pegawai=gaji_baru.pegawai, 
                bulan=gaji_baru.bulan
            ).exists()
            
            if cek_ganda:
                # Jika sudah ada, jangan simpan, beri pesan error (opsional) atau redirect
                return redirect("gaji_list")

            gaji_baru.save()
            return redirect("gaji_list")
    else:
        form = GajiForm()

    return render(request, "laporan/gaji_form.html", {"form": form})

# Edit gaji
def gaji_edit(request, pk):
    gaji = get_object_or_404(Gaji, pk=pk)

    if request.method == "POST":
        form = GajiForm(request.POST, instance=gaji)
        if form.is_valid():
            form.save()   # perubahan otomatis tersimpan
            return redirect("gaji_list")
    else:
        form = GajiForm(instance=gaji)

    return render(request, "laporan/gaji_form.html", {"form": form})

# Hapus gaji
def gaji_hapus(request, pk):
    gaji = get_object_or_404(Gaji, pk=pk)

    if request.method == "POST":
        gaji.delete()
        return redirect("gaji_list")

    return render(request, "laporan/gaji_confirm_delete.html", {"object": gaji})
