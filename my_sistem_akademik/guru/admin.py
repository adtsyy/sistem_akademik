from django.contrib import admin
from .models import Absen, Nilai


@admin.register(Absen)
class AbsenAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'pegawai', 'jadwal', 'tanggal', 'status')
    list_filter = ('status', 'tanggal', 'pegawai', 'jadwal')
    search_fields = ('siswa_nama', 'siswanis', 'jadwal_mata_pelajaran')
    date_hierarchy = 'tanggal'
    ordering = ('-tanggal', 'siswa')


@admin.register(Nilai)
class NilaiAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'pegawai', 'jadwal', 'nilai', 'tanggal')
    list_filter = ('tanggal', 'pegawai', 'jadwal')
    search_fields = ('siswa_nama', 'siswanis', 'jadwal_mata_pelajaran')
    date_hierarchy = 'tanggal'
    ordering = ('-tanggal', 'siswa')
    fieldsets = (
        ('Informasi Siswa', {
            'fields': ('siswa', 'pegawai')
        }),
        ('Pelajaran', {
            'fields': ('jadwal',)
        }),
        ('Nilai', {
            'fields': ('nilai', 'tanggal', 'keterangan')
        }),
    )