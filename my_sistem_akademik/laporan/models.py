from django.db import models
from admin_app.models import Pegawai
from siswa.models import Siswa


# ================= RAPOR =====================
class Rapor(models.Model):
    id_siswa = models.CharField(max_length=20)
    nama = models.CharField(max_length=100)
    kelas = models.CharField(max_length=20)
    nilai_mapel = models.JSONField()
    rata_rata = models.FloatField()
    predikat = models.CharField(max_length=5)
    keterangan = models.CharField(max_length=20)

    def __str__(self):
        return f"Rapor {self.nama} ({self.kelas})"


# ================= SPP =====================
class SPP(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    bulan = models.CharField(max_length=20)
    jumlah = models.IntegerField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.siswa.nama} - {self.bulan}"
    
# ================= GAJI =====================
class Gaji(models.Model):
    pegawai = models.ForeignKey(Pegawai, on_delete=models.CASCADE)
    nama_pegawai = models.CharField(max_length=255, blank=True)  # baru
    gaji_pokok = models.PositiveIntegerField(default=0)
    tunjangan_jabatan = models.PositiveIntegerField(default=0)
    keterangan_tunjangan = models.CharField(max_length=255, blank=True, null=True)

    @property
    def total_gaji(self):
        return self.gaji_pokok + self.tunjangan_jabatan
    
    def save(self, *args, **kwargs):
        # jika gaji_pokok belum diisi, ambil dari pegawai
        if not self.gaji_pokok and self.pegawai:
            self.gaji_pokok = self.pegawai.gaji_pokok
        super().save(*args, **kwargs)

    def __str__(self):
        if self.pegawai:
            return f"Gaji {self.pegawai.nama}"
        return "Gaji (Pegawai belum diisi)"