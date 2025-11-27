from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Rapor, SPP, Gaji
from .forms import RaporForm, SPPForm, GajiForm

# ================= HOME =====================
def home(request):
    return render(request, 'laporan/home.html')

# ================= RAPOR =====================
class RaporListView(ListView):
    model = Rapor
    template_name = 'laporan/rapor_list.html'
    context_object_name = 'rapor'

    def get_queryset(self):
        queryset = super().get_queryset()
        id_siswa = self.request.GET.get('id_siswa')
        if id_siswa:
            queryset = queryset.filter(id_siswa__icontains=id_siswa)
        return queryset
    
class RaporCreateView(CreateView):
    model = Rapor
    form_class = RaporForm
    template_name = 'laporan/rapor_form.html'
    success_url = reverse_lazy('rapor_list')

class RaporUpdateView(UpdateView):
    model = Rapor
    form_class = RaporForm
    template_name = 'laporan/rapor_form.html'
    success_url = reverse_lazy('rapor_list')

class RaporDeleteView(DeleteView):
    model = Rapor
    template_name = 'laporan/rapor_confirm_delete.html'
    success_url = reverse_lazy('rapor_list')

class RaporDetailView(DetailView):
    model = Rapor
    template_name = 'laporan/rapor_detail.html'
    context_object_name = 'rapor'

# ================= SPP =====================
class SPPListView(ListView):
    model = SPP
    template_name = 'laporan/spp_list.html'
    context_object_name = 'spp'

    def get_queryset(self):
        queryset = super().get_queryset()
        id_siswa = self.request.GET.get('id_siswa')
        if id_siswa:
            queryset = queryset.filter(id_siswa__icontains=id_siswa)
        return queryset

class SPPCreateView(CreateView):
    model = SPP
    form_class = SPPForm
    template_name = 'laporan/spp_form.html'
    success_url = reverse_lazy('spp_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bulan_list'] = [
            "Januari","Februari","Maret","April","Mei","Juni",
            "Juli","Agustus","September","Oktober","November","Desember"
        ]
        return context

class SPPUpdateView(UpdateView):
    model = SPP
    form_class = SPPForm
    template_name = 'laporan/spp_form.html'
    success_url = reverse_lazy('spp_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bulan_list'] = [
            "Januari","Februari","Maret","April","Mei","Juni",
            "Juli","Agustus","September","Oktober","November","Desember"
        ]
        return context

class SPPDeleteView(DeleteView):
    model = SPP
    template_name = 'laporan/spp_confirm_delete.html'
    success_url = reverse_lazy('spp_list')


# ================= GAJI =====================

# ===============================
# Tambah gaji
# ===============================
def gaji_tambah(request):
    if request.method == "POST":
        form = GajiForm(request.POST)
        if form.is_valid():
            gaji = form.save(commit=False)
            gaji.nama_pegawai = gaji.pegawai.nama  # simpan nama pegawai
            gaji.save()
            return redirect("gaji_list")
    else:
        form = GajiForm()
    return render(request, "laporan/gaji_form.html", {"form": form})
# ===============================
# Edit gaji
# ===============================
def gaji_edit(request, pk):
    gaji = get_object_or_404(Gaji, pk=pk)
    if request.method == "POST":
        form = GajiForm(request.POST, instance=gaji)
        if form.is_valid():
            form.save()  # simpan perubahan, termasuk gaji_pokok
            return redirect("gaji_list")
    else:
        form = GajiForm(instance=gaji)  # form sudah terisi dengan data database
    return render(request, "laporan/gaji_form.html", {"form": form})

# ===============================
# List gaji
# ===============================
def gaji_list(request):
    gaji = Gaji.objects.all()
    return render(request, "laporan/gaji_list.html", {"gaji": gaji})

# ===============================
# Hapus gaji
# ===============================
def gaji_hapus(request, pk):
    gaji = get_object_or_404(Gaji, pk=pk)
    if request.method == "POST":
        gaji.delete()
        return redirect("gaji_list")
    return render(request, "laporan/gaji_confirm_delete.html", {"object": gaji})