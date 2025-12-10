from django.db import models
from admin_app.models import Jadwal as AdminJadwal


class Siswa(models.Model):
    nis = models.CharField(max_length=10, primary_key=True)
    nama = models.CharField(max_length=100)

    # Kelas disimpan sebagai TEXT (bukan relasi)
    kelas = models.CharField(max_length=20, blank=True)

    tempat_lahir = models.CharField(max_length=100, blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    alamat = models.TextField(blank=True)
    telepon = models.CharField(max_length=15, blank=True)
    nama_orang_tua = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Relasi ke User Django
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):   # FIX: _str_ → __str__
        return f"{self.nama} ({self.nis})"

    class Meta:
        verbose_name_plural = "Siswa"

    # ================================
    # ✔ Tambahan: Ambil jadwal otomatis
    # ================================
    @property
    def jadwal(self):
        """Mengambil jadwal berdasarkan kelas siswa."""
        if not self.kelas:
            return AdminJadwal.objects.none()
        return AdminJadwal.objects.filter(kelas=self.kelas).order_by('hari', 'jam_mulai')


class SPP(models.Model):
    STATUS_CHOICES = [
        ('lunas', 'Lunas'),
        ('belum', 'Belum Bayar'),
    ]

    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, related_name='spp_siswa')
    bulan = models.IntegerField()  # 1-12
    tahun = models.IntegerField()
    nominal = models.DecimalField(max_digits=10, decimal_places=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='belum')
    tanggal_bayar = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):   # FIX: _str_ → __str__
        return f"SPP {self.siswa.nama} - {self.bulan}/{self.tahun}"

    class Meta:
        verbose_name_plural = "SPP"
        ordering = ['-tahun', '-bulan']


# ============================================================
# ✅ MODEL NILAI — Sudah diimplementasikan langsung di bawah sini
# ============================================================
class Nilai(models.Model):
    JENIS_NILAI = [
        ('UH', 'Ulangan Harian'),
        ('UTS', 'UTS'),
        ('UAS', 'UAS'),
    ]

    siswa = models.ForeignKey(
        Siswa,
        on_delete=models.CASCADE,
        related_name='nilai_siswa'
    )

    # Mengambil mapel dari model Jadwal admin
    mapel = models.ForeignKey(
        AdminJadwal,
        on_delete=models.CASCADE,
        related_name='nilai_mapel'
    )

    nilai = models.IntegerField()
    jenis = models.CharField(max_length=10, choices=JENIS_NILAI)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.siswa.nama} - {self.mapel.mapel} - {self.nilai}"

    class Meta:
        verbose_name_plural = "Nilai"
        ordering = ['mapel__hari', 'mapel__jam_mulai']
