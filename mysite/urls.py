from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Tambahkan path autentikasi bawaan Django (login/logout)
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    path('profil/', views.profil_detail, name='profil'),
    path('materi/', views.materi_kuliah, name='materi'),
    path('video/', views.video_gallery, name='video'),
    path('contact/', views.contact, name='contact'),
    path('kegiatan/<slug:slug>/', views.detail_kegiatan, name='detail_kegiatan'),
    
    #Absensi
    path('absensi/', views.daftar_absensi, name='daftar_absensi'),
    path('absensi/input/<int:kelas_id>/', views.input_absensi, name='input_absensi'),
    
]

# Untuk menyajikan file media saat development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)