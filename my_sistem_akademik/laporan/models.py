from django.db import models

# RAPOR
class Rapor(models.Model):
    id_siswa = models.CharField(max_length=20)
    nama = models.CharField(max_length=100)
    kelas = models.CharField(max_length=20)
    nilai_mapel = models.JSONField()
    rata_rata = models.FloatField()
    predikat = models.CharField(max_length=5)
    keterangan = models.CharField(max_length=20)

    def __str__(self):
        return f"Rapor {self.nama}"

# SPP
class SPP(models.Model):
    id_siswa = models.CharField(max_length=20)
    nama = models.CharField(max_length=100)
    bulan = models.CharField(max_length=20)
    jumlah = models.IntegerField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"SPP {self.nama} - {self.bulan}"

# GAJI GURU
class GajiGuru(models.Model):
    id_guru = models.CharField(max_length=20)
    nama = models.CharField(max_length=100)
    gaji_pokok = models.IntegerField()
    tunjangan = models.IntegerField(default=0)
    jabatan_tambahan = models.CharField(max_length=100, null=True, blank=True)
    total_gaji = models.IntegerField()

    def save(self, *args, **kwargs):
        self.total_gaji = self.gaji_pokok + self.tunjangan
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Gaji {self.nama}"
