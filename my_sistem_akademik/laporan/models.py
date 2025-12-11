from django.db import models
from admin_app.models import Pegawai
from siswa.models import Siswa

class Rapor(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, related_name='rapor_siswa')
    nama = models.CharField(max_length=100)
    kelas = models.CharField(max_length=20)
    
    nilai_mapel = models.JSONField()           
    rata_rata = models.FloatField()
    predikat = models.CharField(max_length=5)
    keterangan = models.CharField(max_length=50) 
    
    created_at = models.DateTimeField(auto_now_add=True) # Untuk tahu kapan dibuat
    @property
    def warna_badge(self):
        if self.predikat == 'A':
            return '#28a745'
        elif self.predikat == 'B':
            return '#17a2b8'
        elif self.predikat == 'C':
            return '#ffc107'
        elif self.predikat == 'D':
            return '#dc3545'
        else:
            return '#6c757d'

    def __str__(self):
        return f"Rapor {self.siswa.nama} ({self.kelas})"

class SPP(models.Model):
    BULAN_PILIHAN = [
        (1, 'Januari'), (2, 'Februari'), (3, 'Maret'),
        (4, 'April'), (5, 'Mei'), (6, 'Juni'),
        (7, 'Juli'), (8, 'Agustus'), (9, 'September'),
        (10, 'Oktober'), (11, 'November'), (12, 'Desember'),
    ]

    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, related_name='spp_siswa')
    bulan = models.IntegerField(choices=BULAN_PILIHAN)
    
    # 1. Tambah kolom Tagihan 
    tagihan = models.IntegerField(default=500000, verbose_name="Biaya SPP") 
    
    # 2. Jumlah adalah uang yang dibayarkan siswa
    jumlah = models.IntegerField(verbose_name="Uang Dibayar") 
    
    # 3. Status tidak perlu choices, karena diisi sistem
    status = models.CharField(max_length=50, blank=True) 

    def save(self, *args, **kwargs):
        if self.jumlah >= self.tagihan:
            self.status = 'Lunas'
        else:
            kurang = self.tagihan - self.jumlah
            self.status = f'Belum Lunas (Kurang {kurang:,})'
            
        super(SPP, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.siswa.nama} - {self.bulan}"

class Gaji(models.Model):
    BULAN_PILIHAN = [
        ('Januari', 'Januari'), ('Februari', 'Februari'), ('Maret', 'Maret'),
        ('April', 'April'), ('Mei', 'Mei'), ('Juni', 'Juni'),
        ('Juli', 'Juli'), ('Agustus', 'Agustus'), ('September', 'September'),
        ('Oktober', 'Oktober'), ('November', 'November'), ('Desember', 'Desember'),
    ]

    STATUS_TRANSFER = [
        ('Belum Ditransfer', 'Belum Ditransfer'),
        ('Sudah Ditransfer', 'Sudah Ditransfer'),
    ]

    pegawai = models.ForeignKey(Pegawai, on_delete=models.CASCADE)
    nama_pegawai = models.CharField(max_length=255, blank=True)
    
    bulan = models.CharField(max_length=20, choices=BULAN_PILIHAN, default='Januari')
    status_transfer = models.CharField(max_length=20, choices=STATUS_TRANSFER, default='Belum Ditransfer')

    gaji_pokok = models.PositiveIntegerField(default=0)
    tunjangan_jabatan = models.PositiveIntegerField(default=0)
    keterangan_tunjangan = models.CharField(max_length=255, blank=True, null=True)

    @property
    def total_gaji(self):
        return self.gaji_pokok + self.tunjangan_jabatan

    def save(self, *args, **kwargs):
        if self.pegawai:
            self.nama_pegawai = self.pegawai.nama
            jabatan = self.pegawai.jabatan.lower() 

            if "guru" in jabatan:
                self.gaji_pokok = 3000000
            elif "admin" in jabatan:
                self.gaji_pokok = 2500000
            elif "staff" in jabatan:
                self.gaji_pokok = 2000000
            else:
                self.gaji_pokok = 2000000 

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Gaji {self.nama_pegawai} - {self.bulan}"