from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Rapor, SPP, Gaji
from .forms import RaporForm, SPPForm, GajiForm
from siswa.models import Siswa

def home(request):
    return render(request, 'laporan/home.html')

# List data rapor
class RaporListView(ListView):
    model = Rapor
    template_name = 'laporan/rapor_list.html'
    context_object_name = 'rapor'

    # Fitur pencarian berdasarkan ID siswa
    def get_queryset(self):
        queryset = super().get_queryset()
        id_siswa = self.request.GET.get('id_siswa')
        if id_siswa:
            queryset = queryset.filter(id_siswa__icontains=id_siswa)
        return queryset
    
# Tambah rapor
class RaporCreateView(CreateView):
    model = Rapor
    form_class = RaporForm
    template_name = 'laporan/rapor_form.html'
    success_url = reverse_lazy('rapor_list')

# Edit rapor
class RaporUpdateView(UpdateView):
    model = Rapor
    form_class = RaporForm
    template_name = 'laporan/rapor_form.html'
    success_url = reverse_lazy('rapor_list')

# Hapus rapor
class RaporDeleteView(DeleteView):
    model = Rapor
    template_name = 'laporan/rapor_confirm_delete.html'
    success_url = reverse_lazy('rapor_list')

# Detail rapor
class RaporDetailView(DetailView):
    model = Rapor
    template_name = 'laporan/rapor_detail.html'
    context_object_name = 'rapor'

# List SPP
def spp_list(request):
    spp = SPP.objects.select_related('siswa').all()
    return render(request, 'laporan/spp_list.html', {'spp': spp})

# Tambah SPP
def spp_tambah(request):
    siswa_list = Siswa.objects.all()

    if request.method == 'POST':
        data = request.POST.copy()
        
        # Pastikan data siswa terambil dengan benar dari dropdown
        # Jika nama field di HTML adalah 'siswa', ambil ID-nya
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
                # SKENARIO CICILAN:
                # Tambahkan uang yang baru diinput ke jumlah yang sudah ada
                spp_lama.jumlah += spp_baru.jumlah 
                
                # Update tagihan juga jika admin merubahnya di inputan terakhir (opsional)
                spp_lama.tagihan = spp_baru.tagihan 
                
                # Simpan data lama yang sudah diupdate
                # (Otomatis memicu hitungan status di models.py)
                spp_lama.save() 
            else:
                # SKENARIO DATA BARU:
                # Belum ada data, simpan sebagai data baru
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
            siswa_id = request.POST.get("siswa")    # ambil pilihan siswa
            spp.siswa_id = siswa_id                 # set ke model

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

# Tambah gaji
def gaji_tambah(request):
    if request.method == "POST":
        form = GajiForm(request.POST)
        if form.is_valid():
            gaji = form.save(commit=False)
            gaji.nama_pegawai = gaji.pegawai.nama   # simpan nama pegawai
            gaji.save()
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

# List gaji
def gaji_list(request):
    gaji = Gaji.objects.all()
    return render(request, "laporan/gaji_list.html", {"gaji": gaji})

# Hapus gaji
def gaji_hapus(request, pk):
    gaji = get_object_or_404(Gaji, pk=pk)

    if request.method == "POST":
        gaji.delete()
        return redirect("gaji_list")

    return render(request, "laporan/gaji_confirm_delete.html", {"object": gaji})
