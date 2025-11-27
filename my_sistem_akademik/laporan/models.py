from django.db import models
from admin_app.models import Pegawai
from siswa.models import Siswa

class Rapor(models.Model):
    id_siswa = models.CharField(max_length=20)              # ID unik siswa
    nama = models.CharField(max_length=100)                 # Nama siswa
    kelas = models.CharField(max_length=20)                 # Kelas siswa
    nilai_mapel = models.JSONField()                        # Menyimpan nilai mapel 
    rata_rata = models.FloatField()                         # Rata-rata nilai
    predikat = models.CharField(max_length=5)               # Predikat (A, B, C)
    keterangan = models.CharField(max_length=20)            # Keterangan tambahan

    def __str__(self):
        return f"Rapor {self.nama} ({self.kelas})"

class SPP(models.Model):

    # Pilihan dropdown bulan
    BULAN_PILIHAN = [
        ('Januari', 'Januari'),
        ('Februari', 'Februari'),
        ('Maret', 'Maret'),
        ('April', 'April'),
        ('Mei', 'Mei'),
        ('Juni', 'Juni'),
        ('Juli', 'Juli'),
        ('Agustus', 'Agustus'),
        ('September', 'September'),
        ('Oktober', 'Oktober'),
        ('November', 'November'),
        ('Desember', 'Desember'),
    ]

    # Pilihan status pembayaran
    STATUS_PILIHAN = [
        ('Lunas', 'Lunas'),
        ('Belum Lunas', 'Belum Lunas'),
    ]

    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)        # Relasi ke tabel siswa
    bulan = models.CharField(max_length=20, choices=BULAN_PILIHAN)    # Bulan pembayaran
    jumlah = models.IntegerField()                                     # Nominal SPP
    status = models.CharField(max_length=20, choices=STATUS_PILIHAN)   # Status pembayaran

    def __str__(self):
        return f"{self.siswa.nama} - {self.bulan}"

class Gaji(models.Model):
    pegawai = models.ForeignKey(Pegawai, on_delete=models.CASCADE)     # Pegawai penerima gaji
    nama_pegawai = models.CharField(max_length=255, blank=True)        # Nama pegawai 
    gaji_pokok = models.PositiveIntegerField(default=0)                # Gaji pokok
    tunjangan_jabatan = models.PositiveIntegerField(default=0)         # Tunjangan jabatan
    keterangan_tunjangan = models.CharField(max_length=255, blank=True, null=True)   # Keterangan tambahan

    @property
    def total_gaji(self):
        # Total gaji = gaji pokok + tunjangan
        return self.gaji_pokok + self.tunjangan_jabatan

    def save(self, *args, **kwargs):
        # Jika gaji_pokok belum diisi, otomatis ambil dari data Pegawai
        if not self.gaji_pokok and self.pegawai:
            self.gaji_pokok = self.pegawai.gaji_pokok
        super().save(*args, **kwargs)

    def __str__(self):
        if self.pegawai:
            return f"Gaji {self.pegawai.nama}"
        return "Gaji (Pegawai belum diisi)"
