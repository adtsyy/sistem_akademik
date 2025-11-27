from django.contrib import admin
from .models import Rapor, SPP, Gaji

admin.site.register(Rapor)
admin.site.register(SPP)
@admin.register(Gaji)
class GajiAdmin(admin.ModelAdmin):
    # Kolom yang ditampilkan di halaman list admin
    list_display = ('pegawai', 'gaji_pokok', 'tunjangan_jabatan', 'total_gaji')

    # Field yang tidak bisa diedit (readonly)
    readonly_fields = ('total_gaji',)
