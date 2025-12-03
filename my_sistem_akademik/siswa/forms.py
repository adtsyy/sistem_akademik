from django import forms
from .models import Siswa

# PENTING: JANGAN import model Kelas di bagian paling atas (Global)
# from admin_app.models import Kelas  <-- INI AKAN BIKIN ERROR

class SiswaForm(forms.ModelForm):
    class Meta:
        model = Siswa
        fields = '__all__'
        
        # 1. KITA KECUALIKAN DULU 'kelas_obj' DARI PROSES OTOMATIS
        # Agar saat server start, Django tidak panik mencari admin_app
        exclude = ['kelas_obj'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 2. IMPORT MODEL KELAS DI DALAM FUNGSI (Lazy Import)
        # Import ini baru jalan saat halaman dibuka, bukan saat server start
        # Saat halaman dibuka, admin_app pasti sudah siap.
        try:
            from admin_app.models import Kelas
            queryset_kelas = Kelas.objects.all()
        except ImportError:
            queryset_kelas = []

        # 3. TAMBAHKAN FIELD 'kelas_obj' SECARA MANUAL DI SINI
        self.fields['kelas_obj'] = forms.ModelChoiceField(
            queryset=queryset_kelas,
            required=False,
            label="Kelas",
            widget=forms.Select(attrs={'class': 'form-control'}) # Sesuaikan styling jika perlu
        )