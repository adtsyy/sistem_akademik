from django import forms
from .models import Pegawai, Jadwal

class PegawaiForm(forms.ModelForm):
    class Meta:
        model = Pegawai
        fields = ["nama", "jabatan", "gaji_pokok"]

class JadwalForm(forms.ModelForm):
    class Meta:
        model = Jadwal
        fields = ["hari", "jam_mulai", "jam_selesai", "mata_pelajaran", "pegawai"]