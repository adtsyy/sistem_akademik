from django import forms
from .models import Siswa

class SiswaForm(forms.ModelForm):
    class Meta:
        model = Siswa
        fields = ['nama', 'nis', 'kelas', 'alamat', 'tanggal_lahir']
