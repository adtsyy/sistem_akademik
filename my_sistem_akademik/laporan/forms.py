from django import forms
from .models import Rapor, SPP, Gaji
from .models import Siswa

class RaporForm(forms.ModelForm):
    class Meta:
        model = Rapor
        fields = '__all__'   # Menggunakan semua field dari model Rapor

class SPPForm(forms.ModelForm):
    class Meta:
        model = SPP
        fields = ['siswa', 'bulan', 'tagihan', 'jumlah'] 
        
    widgets = {
        'tagihan': forms.NumberInput(attrs={'placeholder': 'Biaya SPP seharusnya'}),
        'jumlah': forms.NumberInput(attrs={'placeholder': 'Uang yang dibayarkan'}),
    }

class GajiForm(forms.ModelForm):
    class Meta:
        model = Gaji
        fields = ['pegawai', 'bulan', 'tunjangan_jabatan', 'keterangan_tunjangan', 'status_transfer']

    widgets = {
        'tunjangan_jabatan': forms.NumberInput(attrs={'placeholder': 'Contoh: 500000'}),
        'keterangan_tunjangan': forms.TextInput(attrs={'placeholder': 'Contoh: Pembina Pramuka'}),
    }

class RaporSearchForm(forms.Form):
    id_siswa = forms.CharField(
        max_length=20,
        required=False,
        label='ID Siswa'    
    )

class SPPSearchForm(forms.Form):
    id_siswa = forms.CharField(
        max_length=20,
        required=False,
        label='ID Siswa'    
    )

class GajiSearchForm(forms.Form):
    id_pegawai = forms.CharField(
        max_length=20,
        required=False,
        label='ID Pegawai'   
    )
