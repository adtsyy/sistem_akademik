from django.db import models

# Create your models here.
from django.db import models

class Siswa(models.Model):
    nis = models.CharField(max_length=10, primary_key=True)  # jadikan primary key
    nama = models.CharField(max_length=100)
    kelas = models.CharField(max_length=20, blank=True)
    alamat = models.TextField(blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nama} ({self.nis})"