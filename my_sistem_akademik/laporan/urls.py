from django.urls import path
from . import views

urlpatterns = [
    # /laporan/ -> halaman home
    path('', views.home, name='laporan_home'),

    # Rapor
   # --- RAPOR ---
    path('rapor/', views.RaporListView.as_view(), name='rapor_list'),
    # Flow baru: Cari -> Generate
    path('rapor/tambah/', views.tambah_rapor_step1, name='rapor_tambah'), 
    path('rapor/generate/<str:id_siswa>/', views.generate_rapor_siswa, name='rapor_generate'),
    path('rapor/hapus/<int:pk>/', views.RaporDeleteView.as_view(), name='rapor_hapus'),
    path('rapor/detail/<int:pk>/', views.RaporDetailView.as_view(), name='rapor_detail'),
    path('rapor/edit/<int:pk>/', views.RaporUpdateView.as_view(), name='rapor_edit'),

    # SPP
    path('spp/', views.spp_list, name='spp_list'),
    path('spp/tambah/', views.spp_tambah, name='spp_tambah'),
    path('spp/edit/<int:id>/', views.spp_edit, name='spp_edit'),
    path('spp/hapus/<int:id>/', views.spp_hapus, name='spp_hapus'),

    # Gaji
    path("gaji/", views.gaji_list, name="gaji_list"),
    path("gaji/tambah/", views.gaji_tambah, name="gaji_tambah"),
    path("gaji/edit/<int:pk>/", views.gaji_edit, name="gaji_edit"),
    path('gaji/hapus/<int:pk>/', views.gaji_hapus, name='gaji_hapus'),
]
