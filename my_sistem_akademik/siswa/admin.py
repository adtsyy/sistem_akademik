from django.contrib import admin
from .models import Siswa

@admin.register(Siswa)
class SiswaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nis', 'kelas', 'tanggal_lahir')
    search_fields = ('nama', 'nis')
    list_filter = ('kelas',)