from django.urls import path
from . import views

urlpatterns = [
    # /laporan/ -> halaman home
    path('', views.home, name='laporan_home'),  # <-- ini

    # Rapor
    path('rapor/', views.RaporListView.as_view(), name='rapor_list'),
    path('rapor/tambah/', views.RaporCreateView.as_view(), name='rapor_tambah'),
    path('rapor/edit/<int:pk>/', views.RaporUpdateView.as_view(), name='rapor_edit'),
    path('rapor/hapus/<int:pk>/', views.RaporDeleteView.as_view(), name='rapor_hapus'),

    # SPP
    path('spp/', views.SPPListView.as_view(), name='spp_list'),
    path('spp/tambah/', views.SPPCreateView.as_view(), name='spp_tambah'),
    path('spp/edit/<int:pk>/', views.SPPUpdateView.as_view(), name='spp_edit'),
    path('spp/hapus/<int:pk>/', views.SPPDeleteView.as_view(), name='spp_hapus'),

    # Gaji
    path('gaji/', views.GajiListView.as_view(), name='gaji_list'),
    path('gaji/tambah/', views.GajiCreateView.as_view(), name='gaji_tambah'),
    path('gaji/edit/<int:pk>/', views.GajiUpdateView.as_view(), name='gaji_edit'),
    path('gaji/hapus/<int:pk>/', views.GajiDeleteView.as_view(), name='gaji_hapus'),
]
