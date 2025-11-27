from django.contrib import admin
from .models import Rapor, SPP, Gaji

admin.site.register(Rapor)
admin.site.register(SPP)

@admin.register(Gaji)
class GajiAdmin(admin.ModelAdmin):
    list_display = ('pegawai', 'gaji_pokok', 'tunjangan_jabatan', 'total_gaji')
    readonly_fields = ('total_gaji',)
