
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Pegawai, Jadwal


class PegawaiForm(forms.ModelForm):
    username = forms.CharField(required=False, max_length=150, label='Username (opsional)')
    password = forms.CharField(required=False, widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput, label='Konfirmasi Password')

    class Meta:
        model = Pegawai
        fields = ["nama", "jabatan"]

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        # Jika instance sudah punya user, isi initial username
        instance = kwargs.get('instance')
        if instance and getattr(instance, 'user', None):
            self.fields['username'].initial = instance.user.username

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            qs = User.objects.filter(username=username)
            # Jika editing, exclude current linked user
            instance = getattr(self, 'instance', None)
            if instance and instance.user:
                qs = qs.exclude(pk=instance.user.pk)
            if qs.exists():
                raise ValidationError('Username sudah digunakan.')
        return username

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get('password')
        confirm = cleaned.get('confirm_password')
        username = cleaned.get('username')

        # Jika username disediakan, biarkan password kosong (akan jadi unusable)
        if password or confirm:
            if password != confirm:
                raise ValidationError('Password dan konfirmasi tidak cocok.')

        return cleaned

    def save(self, commit=True):
        # Simpan Pegawai dulu tanpa commit ke DB jika perlu
        pegawai = super().save(commit=False)

        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username:
            # Update existing user jika ada
            if pegawai.user:
                user = pegawai.user
                if user.username != username:
                    user.username = username
                if password:
                    user.set_password(password)
                # set role: admin -> is_staff True, guru/staff -> is_staff False
                user.is_staff = True if pegawai.jabatan == 'admin' else False
                user.save()
            else:
                # Buat user baru
                if password:
                    user = User.objects.create_user(username=username, password=password)
                else:
                    # buat user tanpa password yang dapat diubah kemudian
                    user = User.objects.create_user(username=username)
                    user.set_unusable_password()
                    user.save()
                user.is_staff = True if pegawai.jabatan == 'admin' else False
                user.save()
                pegawai.user = user
        else:
            # Jika tidak ada username namun sebelumnya terhubung ke user, jangan otomatis hapus
            pass

        if commit:
            pegawai.save()

        return pegawai

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