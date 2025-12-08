from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Siswa

class SiswaForm(forms.ModelForm):
    # 1. Tambahan Field untuk Login (Username & Password)
    username = forms.CharField(
        required=False, 
        label='Username (Untuk Login)',
        widget=forms.TextInput(attrs={
            'style': 'background: #0f1f2e; color: white; border: 1px solid #415a77; padding: 10px; border-radius: 6px; width: 100%;',
            'placeholder': 'Buat Username Unik'
        })
    )
    password = forms.CharField(
        required=False, 
        label='Password',
        widget=forms.PasswordInput(attrs={
            'style': 'background: #0f1f2e; color: white; border: 1px solid #415a77; padding: 10px; border-radius: 6px; width: 100%;',
            'placeholder': 'Masukkan Password'
        })
    )
    confirm_password = forms.CharField(
        required=False, 
        label='Konfirmasi Password',
        widget=forms.PasswordInput(attrs={
            'style': 'background: #0f1f2e; color: white; border: 1px solid #415a77; padding: 10px; border-radius: 6px; width: 100%;',
            'placeholder': 'Ulangi Password'
        })
    )

    class Meta:
        model = Siswa
        fields = '__all__'
        # Kita exclude 'user' agar tidak muncul dropdown user di form html
        exclude = ['user'] 
        
        widgets = {
            'nis': forms.TextInput(attrs={'style': 'background: #0f1f2e; color: white; border: 1px solid #415a77; padding: 10px; border-radius: 6px; width: 100%;'}),
            'nama': forms.TextInput(attrs={'style': 'background: #0f1f2e; color: white; border: 1px solid #415a77; padding: 10px; border-radius: 6px; width: 100%;'}),
            'kelas': forms.TextInput(attrs={'placeholder': 'Contoh: XII IPA 1', 'style': 'background: #0f1f2e; color: white; border: 1px solid #415a77; padding: 10px; border-radius: 6px; width: 100%;'}),
            'tempat_lahir': forms.TextInput(attrs={'style': 'background: #0f1f2e; color: white; border: 1px solid #415a77; padding: 10px; border-radius: 6px; width: 100%;'}),
            'tanggal_lahir': forms.DateInput(attrs={'type': 'date', 'style': 'background: #0f1f2e; color: white; border: 1px solid #415a77; padding: 10px; border-radius: 6px; width: 100%;'}),
            'alamat': forms.Textarea(attrs={'rows': 3, 'style': 'background: #0f1f2e; color: white; border: 1px solid #415a77; padding: 10px; border-radius: 6px; width: 100%;'}),
            'telepon': forms.TextInput(attrs={'style': 'background: #0f1f2e; color: white; border: 1px solid #415a77; padding: 10px; border-radius: 6px; width: 100%;'}),
            'nama_orang_tua': forms.TextInput(attrs={'style': 'background: #0f1f2e; color: white; border: 1px solid #415a77; padding: 10px; border-radius: 6px; width: 100%;'}),
            'jurusan': forms.TextInput(attrs={'style': 'background: #0f1f2e; color: white; border: 1px solid #415a77; padding: 10px; border-radius: 6px; width: 100%;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Jika sedang edit siswa dan siswa sudah punya user, isi field username otomatis
        instance = kwargs.get('instance')
        if instance and instance.user:
            self.fields['username'].initial = instance.user.username

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            qs = User.objects.filter(username=username)
            # Jika sedang mode edit, jangan cek username milik sendiri
            instance = getattr(self, 'instance', None)
            if instance and instance.user:
                qs = qs.exclude(pk=instance.user.pk)
            
            if qs.exists():
                raise ValidationError('Username sudah digunakan oleh orang lain.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password or confirm_password:
            if password != confirm_password:
                raise ValidationError('Password dan konfirmasi tidak cocok.')
        return cleaned_data

    def save(self, commit=True):
        # 1. Simpan data Siswa (nis, nama, dll) tapi jangan commit ke DB dulu
        siswa = super().save(commit=False)

        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username:
            # Jika siswa sudah punya user (Mode Edit)
            if siswa.user:
                user = siswa.user
                user.username = username
                if password: # Cuma update password kalau diisi
                    user.set_password(password)
                user.save()
            
            # Jika siswa belum punya user (Mode Tambah Baru)
            else:
                if password:
                    user = User.objects.create_user(username=username, password=password)
                else:
                    # Buat user tanpa password (kasus jarang, tapi jaga-jaga)
                    user = User.objects.create_user(username=username)
                    user.set_unusable_password()
                
                # PENTING: Siswa bukan staff/admin
                user.is_staff = False 
                user.save()
                
                # Hubungkan Siswa ke User yang baru dibuat
                siswa.user = user
        
        if commit:
            siswa.save()

        return siswa