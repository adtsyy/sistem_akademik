# # my_sistem_akademik/urls.py
# from django.contrib import admin
# from django.urls import path, include
# from my_sistem_akademik import views  # pastikan views login/logout ada di sini

# urlpatterns = [
#     # Admin default Django
#     path('admin/', admin.site.urls),

#     # Auth
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),

#     # Aplikasi
#     path('admin_app/', include('admin_app.urls')),  # dashboard/admin_app
#     path('guru/', include('guru.urls')),           # dashboard/guru
#     path('laporan/', include('laporan.urls')),     # halaman laporan
#     path('siswa/', include('siswa.urls'))
# ]

# my_sistem_akademik/urls.py
from django.contrib import admin
from django.urls import path, include
from my_sistem_akademik import views  # pastikan views login/logout ada di sini

urlpatterns = [
    # Root
    path('', views.redirect_to_login, name='home'),
    
    # Admin default Django
    path('admin/', admin.site.urls),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Aplikasi
    path('admin_app/', include('admin_app.urls')),  # dashboard/admin_app
    path('guru/', include('guru.urls')),           # dashboard/guru
    path('laporan/', include('laporan.urls')),     # halaman laporan
    path('siswa/', include('siswa.urls'))
]