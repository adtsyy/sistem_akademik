from django import forms
from .models import Pegawai, Jadwal

class PegawaiForm(forms.ModelForm):
    class Meta:
        model = Pegawai
        fields = ["nama", "jabatan"]

class JadwalForm(forms.ModelForm):
    class Meta:
        model = Jadwal
        # Tambahkan "kelas" di sini agar muncul di form HTML
        fields = ["hari", "jam_mulai", "jam_selesai", "mata_pelajaran", "kelas", "pegawai"]
        
        # Opsional: Tambahkan widgets agar input jam lebih rapi (tipe time)
        widgets = {
            'jam_mulai': forms.TimeInput(attrs={'type': 'time'}),
            'jam_selesai': forms.TimeInput(attrs={'type': 'time'}),
            'kelas': forms.TextInput(attrs={
                'placeholder': 'Contoh: XII IPA 1', 
                'style': 'color: white; background: rgba(255,255,255,0.1); border: none;'}),
        }