from django import forms
from .models import Rapor, SPP, Gaji

class RaporForm(forms.ModelForm):
    class Meta:
        model = Rapor
        fields = '__all__'

class SPPForm(forms.ModelForm):
    class Meta:
        model = SPP
        fields = ['id_siswa', 'nama', 'bulan', 'jumlah', 'status']
        widgets = {
            'status': forms.Select(choices=[('Lunas','Lunas'), ('Belum Lunas','Belum Lunas')])
        }

class GajiForm(forms.ModelForm):
    class Meta:
        model = Gaji
        fields = '__all__'
