from django.db import models
from django.contrib.auth.models import User

class Kelas(models.Model):
    nama_kelas = models.CharField(max_length=50)
    # Tambahkan field lain jika perlu, misal wali_kelas

    def __str__(self):
        return self.nama_kelas

class Pegawai(models.Model):
    id_pegawai = models.CharField(max_length=10, unique=True, editable=False)

    JABATAN_CHOICES = [
        ("guru", "Guru"),
        ("staff", "Staff"),
        ("admin", "Admin"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nama = models.CharField(max_length=200)
    nip = models.CharField(max_length=50, blank=True, null=True)
    jabatan = models.CharField(max_length=20, choices=JABATAN_CHOICES)
    gaji_pokok = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.id_pegawai:  # generate ID jika belum ada
            last_id = Pegawai.objects.order_by('-id_pegawai').first()
            if last_id:
                number = int(last_id.id_pegawai[1:]) + 1
            else:
                number = 1
            self.id_pegawai = f"P{number:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama


class Jadwal(models.Model):
    HARI_CHOICES = [
        ("Senin", "Senin"),
        ("Selasa", "Selasa"),
        ("Rabu", "Rabu"),
        ("Kamis", "Kamis"),
        ("Jumat", "Jumat"),
    ]

    hari = models.CharField(max_length=20, choices=HARI_CHOICES)
    jam_mulai = models.TimeField()
    jam_selesai = models.TimeField()
    mata_pelajaran = models.CharField(max_length=100)
    pegawai = models.ForeignKey(Pegawai, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.mata_pelajaran} - {self.hari}"
