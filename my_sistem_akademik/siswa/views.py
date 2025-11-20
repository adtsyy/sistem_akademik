from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def halaman_siswa(request):
    return HttpResponse("Ini halaman siswa!")
