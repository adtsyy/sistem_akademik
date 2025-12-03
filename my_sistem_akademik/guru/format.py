from django import forms
from .models import Absen, Nilai


class AbsenForm(forms.ModelForm):
    class Meta:
        model = Absen
        fields = ['siswa', 'jadwal', 'tanggal', 'status', 'keterangan']
        widgets = {
            'siswa': forms.Select(attrs={
                'class': 'form-control'
            }),
            'jadwal': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tanggal': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'keterangan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }


class NilaiForm(forms.ModelForm):
    class Meta:
        model = Nilai
        fields = ['siswa', 'jadwal', 'tanggal', 'nilai', 'keterangan']
        widgets = {
            'siswa': forms.Select(attrs={
                'class': 'form-control'
            }),
            'jadwal': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tanggal': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'nilai': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'step': '0.1'
            }),
            'keterangan': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }

    def clean_nilai(self):
        nilai = self.cleaned_data.get('nilai')
        if nilai is not None and (nilai < 0 or nilai > 100):
            raise forms.ValidationError('Nilai harus antara 0 dan 100')
        return nilai