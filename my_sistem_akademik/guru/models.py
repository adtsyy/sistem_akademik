from django.db import models

# Create your models here.
from django.db import models
from admin_app.models import Pegawai, Jadwal
from siswa.models import Siswa
from django.utils import timezone


class Absen(models.Model):
    STATUS_CHOICES = [
        ('hadir', 'Hadir'),
        ('sakit', 'Sakit'),
        ('izin', 'Izin'),
        ('alpa', 'Alpa'),
    ]
    
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    pegawai = models.ForeignKey(Pegawai, on_delete=models.CASCADE)
    jadwal = models.ForeignKey(Jadwal, on_delete=models.CASCADE)
    tanggal = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    keterangan = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('siswa', 'jadwal', 'tanggal')
        ordering = ['-tanggal', 'siswa']
    
    def __str__(self):
        return f"{self.siswa.nama} - {self.jadwal.mata_pelajaran} - {self.tanggal}"


class Nilai(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    pegawai = models.ForeignKey(Pegawai, on_delete=models.CASCADE)
    jadwal = models.ForeignKey(Jadwal, on_delete=models.CASCADE)
    nilai = models.FloatField(validators=[])
    tanggal = models.DateField(default=timezone.now)
    keterangan = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('siswa', 'jadwal', 'tanggal')
        ordering = ['-tanggal', 'siswa']
    
    def __str__(self):
        return f"{self.siswa.nama} - {self.jadwal.mata_pelajaran} - {self.nilai}"