from django.contrib import admin
from .models import Profil, TriDharma, Kegiatan, MataKuliah, Materi, KategoriVideo, VideoYoutube, Mahasiswa, SesiKuliah, Absensi, PerguruanTinggi, Jurusan, Kelas

admin.site.register(Profil)
admin.site.register(TriDharma)
admin.site.register(Kegiatan)
# admin.site.register(MataKuliah)
admin.site.register(Materi)
admin.site.register(KategoriVideo)
admin.site.register(VideoYoutube)

class KelasInline(admin.TabularInline):
    model = Kelas
    extra = 1

@admin.register(MataKuliah)
class MataKuliahAdmin(admin.ModelAdmin):
    list_display = ('kode', 'nama', 'sks')
    inlines = [KelasInline] # Bisa tambah kelas langsung di menu Mata Kuliah

@admin.register(Kelas)
class KelasAdmin(admin.ModelAdmin):
    list_display = ('mata_kuliah', 'nama_kelas', 'semester', 'jumlah_mahasiswa')
    list_filter = ('semester', 'mata_kuliah')
    filter_horizontal = ('mahasiswa',) # Kotak seleksi mahasiswa Pindah ke sini

    def jumlah_mahasiswa(self, obj):
        return obj.mahasiswa.count()

class AbsensiInline(admin.TabularInline):
    model = Absensi
    extra = 0
    can_delete = False
    readonly_fields = ('mahasiswa',)

class MahasiswaAdmin(admin.ModelAdmin):
    list_display = ('nim', 'nama', 'jurusan')
    search_fields = ('nim', 'nama')

@admin.register(SesiKuliah)
class SesiKuliahAdmin(admin.ModelAdmin):
    list_display = ('kelas', 'pertemuan_ke', 'tanggal', 'topik')
    list_filter = ('kelas__mata_kuliah', 'kelas__nama_kelas') # Filter baru
    inlines = [AbsensiInline]

# class SesiKuliahAdmin(admin.ModelAdmin):
#     list_display = ('mata_kuliah', 'pertemuan_ke', 'tanggal', 'topik')
#     list_filter = ('mata_kuliah',)

# class AbsensiAdmin(admin.ModelAdmin):
#     list_display = ('sesi', 'mahasiswa', 'status')
#     list_filter = ('sesi', 'status')

class JurusanAdmin(admin.ModelAdmin):
    list_display = ('nama', 'jenjang', 'perguruan_tinggi')
    list_filter = ('perguruan_tinggi', 'jenjang')
    
admin.site.register(PerguruanTinggi)
admin.site.register(Jurusan, JurusanAdmin)
admin.site.register(Mahasiswa, MahasiswaAdmin)
# admin.site.register(SesiKuliah, SesiKuliahAdmin)
# admin.site.register(Absensi, AbsensiAdmin)
admin.site.register(Absensi)