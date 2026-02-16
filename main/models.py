from django.db import models
from django.contrib.auth.models import User

# 1. Profil Dosen
class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama_lengkap = models.CharField(max_length=100)
    nidn = models.CharField(max_length=20)
    bio = models.TextField()
    foto = models.ImageField(upload_to='profil/', blank=True, null=True)
    email = models.EmailField()
    scholar_link = models.URLField(blank=True, verbose_name="Google Scholar URL")
    
    def __str__(self):
        return self.nama_lengkap

# 2. Tri Dharma (Penelitian, PkM, Publikasi)
class KategoriTriDharma(models.TextChoices):
    PENELITIAN = 'PENELITIAN', 'Penelitian'
    PKM = 'PKM', 'Pengabdian Masyarakat'
    PUBLIKASI = 'PUBLIKASI', 'Publikasi Jurnal/Buku'

class TriDharma(models.Model):
    kategori = models.CharField(max_length=20, choices=KategoriTriDharma.choices)
    judul = models.CharField(max_length=200)
    tahun = models.IntegerField()
    deskripsi = models.TextField(blank=True)
    link_eksternal = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['-tahun']

    def __str__(self):
        return f"{self.kategori} - {self.judul}"
    
# 1. Model Perguruan Tinggi
class PerguruanTinggi(models.Model):
    nama = models.CharField(max_length=200, help_text="Contoh: Universitas Indonesia")
    kode_pt = models.CharField(max_length=20, blank=True, null=True, help_text="Kode PT Dikti (Opsional)")
    alamat = models.TextField(blank=True)

    def __str__(self):
        return self.nama
    
    class Meta:
        verbose_name_plural = "Perguruan Tinggi"

# 2. Model Jurusan (Terkoneksi ke Perguruan Tinggi)
class Jurusan(models.Model):
    perguruan_tinggi = models.ForeignKey(PerguruanTinggi, on_delete=models.CASCADE, related_name='jurusan')
    nama = models.CharField(max_length=100, help_text="Contoh: Teknik Informatika")
    jenjang = models.CharField(max_length=10, choices=[
        ('D3', 'D3'),
        ('S1', 'S1'),
        ('S2', 'S2'),
        ('S3', 'S3'),
    ], default='S1')

    def __str__(self):
        return f"{self.nama} ({self.jenjang}) - {self.perguruan_tinggi.nama}"
    
    class Meta:
        verbose_name_plural = "Jurusan"

# 3. Model Mahasiswa (Diupdate: Jurusan sekarang ForeignKey)
class Mahasiswa(models.Model):
    nama = models.CharField(max_length=100)
    nim = models.CharField(max_length=20, unique=True)
    # PERUBAHAN DISINI: Jurusan bukan lagi teks biasa, tapi relasi ke tabel Jurusan
    jurusan = models.ForeignKey(Jurusan, on_delete=models.SET_NULL, null=True, related_name='mahasiswa')
    
    # Opsional: Foto mahasiswa
    foto = models.ImageField(upload_to='mahasiswa/', blank=True, null=True)

    def __str__(self):
        return f"{self.nim} - {self.nama}"


# 3. Kegiatan Dosen (Berita/Blog)
class Kegiatan(models.Model):
    judul = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    konten = models.TextField()
    tanggal = models.DateField()
    gambar = models.ImageField(upload_to='kegiatan/', blank=True)

    def __str__(self):
        return self.judul

# 4. Materi Kuliah
class MataKuliah(models.Model):
    nama = models.CharField(max_length=100)
    kode = models.CharField(max_length=20)
    sks = models.IntegerField(default=3) # Opsional

    def __str__(self):
        return f"{self.kode} - {self.nama}"

class Kelas(models.Model):
    mata_kuliah = models.ForeignKey(MataKuliah, on_delete=models.CASCADE, related_name='kelas_set')
    nama_kelas = models.CharField(max_length=50, help_text="Contoh: Kelas A, TI-2B, Pagi")
    semester = models.CharField(max_length=20, help_text="Contoh: Ganjil 2023/2024")
    tahun_ajaran = models.CharField(max_length=20, blank=True, null=True)
    
    # LIST MAHASISWA PINDAH KE SINI
    mahasiswa = models.ManyToManyField(Mahasiswa, related_name='kelas_diambil', blank=True)

    def __str__(self):
        return f"{self.mata_kuliah.nama} ({self.nama_kelas}) - {self.semester}"
    
    class Meta:
        verbose_name_plural = "Kelas Perkuliahan"

class Materi(models.Model):
    mata_kuliah = models.ForeignKey(MataKuliah, on_delete=models.CASCADE, related_name='materi')
    judul_materi = models.CharField(max_length=100)
    file_materi = models.FileField(upload_to='materi/')
    tanggal_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mata_kuliah.nama} - {self.judul_materi}"

# 5. Kumpulan Video Youtube
class KategoriVideo(models.Model):
    nama = models.CharField(max_length=50)

    def __str__(self):
        return self.nama

class VideoYoutube(models.Model):
    judul = models.CharField(max_length=100)
    youtube_id = models.CharField(max_length=100, help_text="Contoh: dQw4w9WgXcQ")
    kategori = models.ForeignKey(KategoriVideo, on_delete=models.CASCADE)
    deskripsi = models.TextField(blank=True)

    def __str__(self):
        return self.judul

# 3. Model Sesi Kuliah (Pertemuan)
class SesiKuliah(models.Model):
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, related_name='sesi_set') # Ubah relasi
    topik = models.CharField(max_length=200)
    tanggal = models.DateField()
    pertemuan_ke = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.kelas.nama_kelas} - Pertemuan {self.pertemuan_ke}"

# 4. Model Absensi (Detail Siapa yang Hadir)
class Absensi(models.Model):
    STATUS_CHOICES = [
        ('H', 'Hadir'),
        ('S', 'Sakit'),
        ('I', 'Izin'),
        ('A', 'Alpha'),
    ]
    sesi = models.ForeignKey(SesiKuliah, on_delete=models.CASCADE)
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    keterangan = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ['sesi', 'mahasiswa'] # Satu mahasiswa hanya bisa diabsen sekali per sesi

    def __str__(self):
        return f"{self.mahasiswa.nama} - {self.get_status_display()}"
