from django.shortcuts import render, get_object_or_404, redirect
from .models import Siswa
from .forms import SiswaForm

def list_siswa(request):
    datas = Siswa.objects.all().order_by('-created_at')
    return render(request, 'siswa_app/list.html', {'datas': datas})

def detail_siswa(request, pk):
    s = get_object_or_404(Siswa, pk=pk)
    return render(request, 'siswa_app/detail.html', {'siswa': s})

def create_siswa(request):
    if request.method == 'POST':
        form = SiswaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('siswa:list')
    else:
        form = SiswaForm()
    return render(request, 'siswa_app/form.html', {'form': form, 'title': 'Tambah Siswa'})

def update_siswa(request, pk):
    s = get_object_or_404(Siswa, pk=pk)
    if request.method == 'POST':
        form = SiswaForm(request.POST, instance=s)
        if form.is_valid():
            form.save()
            return redirect('siswa:detail', pk=s.pk)
    else:
        form = SiswaForm(instance=s)
    return render(request, 'siswa_app/form.html', {'form': form, 'title': 'Edit Siswa'})

def delete_siswa(request, pk):
    s = get_object_or_404(Siswa, pk=pk)
    if request.method == 'POST':
        s.delete()
        return redirect('siswa:list')
    return render(request, 'siswa_app/confirm_delete.html', {'object': s})
