from django.shortcuts import render, redirect, get_object_or_404
from .models import Siswa
from .forms import SiswaForm


def siswa_list(request):
    data = Siswa.objects.all()
    return render(request, "siswa_app/list.html", {"siswa": data})


def siswa_tambah(request):
    form = SiswaForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("siswa_list")

    return render(request, "siswa_app/form.html", {
        "title": "Tambah Siswa",
        "form": form,
    })


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


def siswa_detail(request, nis):
    siswa = get_object_or_404(Siswa, nis=nis)
    return render(request, "siswa_app/detail.html", {"siswa": siswa})


def siswa_hapus(request, nis):
    siswa = get_object_or_404(Siswa, nis=nis)

    if request.method == "POST":
        siswa.delete()
        return redirect("siswa_list")

    return render(request, "siswa_app/confirm_delete.html", {"siswa": siswa})
