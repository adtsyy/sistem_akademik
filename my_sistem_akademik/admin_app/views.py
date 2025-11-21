from django.shortcuts import render, redirect, get_object_or_404
from .models import Pegawai, Jadwal
from .forms import PegawaiForm, JadwalForm


# DASHBOARD
def index(request):
    pegawai = Pegawai.objects.all()
    jadwal = Jadwal.objects.all().order_by("hari", "jam_mulai")
    return render(request, "admin_app/index.html", {
        "pegawai_list": pegawai,
        "jadwal_list": jadwal
    })


# PEGAWAI
def list_pegawai(request):
    data = Pegawai.objects.all()
    return render(request, "admin_app/pegawai.html", {"pegawai_list": data})


def tambah_pegawai(request):
    form = PegawaiForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("list_pegawai")
    return render(request, "admin_app/tambah_pegawai.html", {"form": form})


def edit_pegawai(request, id):
    pegawai = get_object_or_404(Pegawai, id=id)
    form = PegawaiForm(request.POST or None, instance=pegawai)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("list_pegawai")
    return render(request, "admin_app/edit_pegawai.html", {"form": form})


def hapus_pegawai(request, id):
    pegawai = get_object_or_404(Pegawai, id=id)
    pegawai.delete()
    return redirect("list_pegawai")


# JADWAL
def list_jadwal(request):
    data = Jadwal.objects.all().order_by("hari", "jam_mulai")
    return render(request, "admin_app/jadwal.html", {"jadwal_list": data})


def tambah_jadwal(request):
    form = JadwalForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("list_jadwal")
    return render(request, "admin_app/tambah_jadwal.html", {"form": form})


def edit_jadwal(request, id):
    jadwal = get_object_or_404(Jadwal, id=id)
    form = JadwalForm(request.POST or None, instance=jadwal)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("list_jadwal")
    return render(request, "admin_app/edit_jadwal.html", {"form": form})


def hapus_jadwal(request, id):
    jadwal = get_object_or_404(Jadwal, id=id)
    jadwal.delete()
    return redirect("list_jadwal")
