from django.db import models

from django.db import models

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

    def __str__(self):
        return f"{self.nama} ({self.nis})"

    class Meta:
        verbose_name_plural = "Siswa"



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

    # PERBAIKAN: Gunakan double underscore (__str__)
    def __str__(self):
        return f"SPP {self.siswa.nama} - {self.bulan}/{self.tahun}"

    class Meta:
        verbose_name_plural = "SPP"
        ordering = ['-tahun', '-bulan']