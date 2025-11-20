from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Rapor, SPP, GajiGuru
from .forms import RaporForm, SPPForm, GajiGuruForm

# ================= HOME =====================
def home(request):
    return render(request, 'laporan/home.html')

# ================= RAPOR =====================
class RaporListView(ListView):
    model = Rapor
    template_name = 'laporan/rapor_list.html'
    context_object_name = 'rapor'

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


# ================= SPP =====================
class SPPListView(ListView):
    model = SPP
    template_name = 'laporan/spp_list.html'
    context_object_name = 'spp'

class SPPCreateView(CreateView):
    model = SPP
    form_class = SPPForm
    template_name = 'laporan/spp_form.html'
    success_url = reverse_lazy('spp_list')

class SPPUpdateView(UpdateView):
    model = SPP
    form_class = SPPForm
    template_name = 'laporan/spp_form.html'
    success_url = reverse_lazy('spp_list')

class SPPDeleteView(DeleteView):
    model = SPP
    template_name = 'laporan/spp_confirm_delete.html'
    success_url = reverse_lazy('spp_list')


# ================= GAJI GURU =====================
class GajiListView(ListView):
    model = GajiGuru
    template_name = 'laporan/gaji_list.html'
    context_object_name = 'gaji'

class GajiCreateView(CreateView):
    model = GajiGuru
    form_class = GajiGuruForm
    template_name = 'laporan/gaji_form.html'
    success_url = reverse_lazy('gaji_list')

class GajiUpdateView(UpdateView):
    model = GajiGuru
    form_class = GajiGuruForm
    template_name = 'laporan/gaji_form.html'
    success_url = reverse_lazy('gaji_list')

class GajiDeleteView(DeleteView):
    model = GajiGuru
    template_name = 'laporan/gaji_confirm_delete.html'
    success_url = reverse_lazy('gaji_list')
