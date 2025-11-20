from django.shortcuts import render
from .models import Rapor, SPP, GajiGuru

def halaman_laporan(request):
    return render(request, 'laporan/home.html')

def daftar_rapor(request):
    data = Rapor.objects.all()
    return render(request, 'laporan/rapor_list.html', {'rapor': data})

def daftar_spp(request):
    data = SPP.objects.all()
    return render(request, 'laporan/spp_list.html', {'spp': data})

def daftar_gaji(request):
    data = GajiGuru.objects.all()
    return render(request, 'laporan/gaji_list.html', {'gaji': data})
