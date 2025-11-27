from django.db import models

class Pegawai(models.Model):
    JABATAN_CHOICES = [
        ("guru", "Guru"),
        ("staff", "Staff"),
        ("admin", "Admin"),
    ]

    nama = models.CharField(max_length=200)
    jabatan = models.CharField(max_length=20, choices=JABATAN_CHOICES)
    gaji_pokok = models.IntegerField(default=0)

    def _str_(self):
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

    def _str_(self):
        return f"{self.mata_pelajaran} - {self.hari}"