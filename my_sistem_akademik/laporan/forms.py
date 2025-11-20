from django import forms
from .models import Rapor, SPP, Gaji

# ================= RAPOR =====================
class RaporForm(forms.ModelForm):
    class Meta:
        model = Rapor
        fields = '__all__'

# ================= SPP =====================
class SPPForm(forms.ModelForm):
    class Meta:
        model = SPP
        fields = ['id_siswa', 'nama', 'bulan', 'jumlah', 'status']
        widgets = {
            'status': forms.Select(choices=SPP.STATUS_CHOICES)
        }

# ================= GAJI =====================
class GajiForm(forms.ModelForm):
    class Meta:
        model = Gaji
        fields = '__all__'

# ================= SEARCH FORMS =====================
class RaporSearchForm(forms.Form):
    id_siswa = forms.CharField(max_length=20, required=False, label='ID Siswa')

class SPPSearchForm(forms.Form):
    id_siswa = forms.CharField(max_length=20, required=False, label='ID Siswa')

class GajiSearchForm(forms.Form):
    id_pegawai = forms.CharField(max_length=20, required=False, label='ID Pegawai')
