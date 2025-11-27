from django.db import models

# Create your models here.
from django.db import models

class Siswa(models.Model):
    nama = models.CharField(max_length=100)
    nis = models.CharField(max_length=20, unique=True)
    kelas = models.CharField(max_length=20, blank=True)
    alamat = models.TextField(blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.nama} ({self.nis})"