from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Rapor, SPP, Gaji
from .forms import RaporForm, SPPForm, GajiForm
from django.views.generic import DetailView

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
class GajiListView(ListView):
    model = Gaji
    template_name = 'laporan/gaji_list.html'
    context_object_name = 'gaji'

    def get_queryset(self):
        queryset = super().get_queryset()
        id_pegawai = self.request.GET.get('id_pegawai')
        if id_pegawai:
            queryset = queryset.filter(id_pegawai__icontains=id_pegawai)
        return queryset

class GajiCreateView(CreateView):
    model = Gaji
    form_class = GajiForm
    template_name = 'laporan/gaji_form.html'
    success_url = reverse_lazy('gaji_list')

class GajiUpdateView(UpdateView):
    model = Gaji
    form_class = GajiForm
    template_name = 'laporan/gaji_form.html'
    success_url = reverse_lazy('gaji_list')

class GajiDeleteView(DeleteView):
    model = Gaji
    template_name = 'laporan/gaji_confirm_delete.html'
    success_url = reverse_lazy('gaji_list')
