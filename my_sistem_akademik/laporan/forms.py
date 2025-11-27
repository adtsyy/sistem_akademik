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
        fields = ['siswa', 'bulan', 'jumlah', 'status']   # Field yang ditampilkan di form

class GajiForm(forms.ModelForm):
    class Meta:
        model = Gaji
        fields = ['pegawai', 'gaji_pokok', 'tunjangan_jabatan', 'keterangan_tunjangan']

        # Widget untuk custom tampilan input
        widgets = {
            'gaji_pokok': forms.NumberInput(attrs={'placeholder': 'Masukkan gaji pokok'}),
        }

class RaporSearchForm(forms.Form):
    id_siswa = forms.CharField(
        max_length=20,
        required=False,
        label='ID Siswa'     # Input pencarian berdasarkan ID siswa
    )

class SPPSearchForm(forms.Form):
    id_siswa = forms.CharField(
        max_length=20,
        required=False,
        label='ID Siswa'     # Input pencarian SPP berdasarkan ID siswa
    )

class GajiSearchForm(forms.Form):
    id_pegawai = forms.CharField(
        max_length=20,
        required=False,
        label='ID Pegawai'   # Input pencarian gaji berdasarkan ID pegawai
    )
