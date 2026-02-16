from django.shortcuts import render, get_object_or_404, redirect
from .models import Profil, TriDharma, Kegiatan, MataKuliah, VideoYoutube, KategoriVideo, Kelas, SesiKuliah, Absensi
from django.contrib.auth.decorators import login_required
from datetime import date


def home(request):
    # Mengambil profil dosen (asumsi hanya ada 1 user admin)
    profil = Profil.objects.first()
    kegiatan_terbaru = Kegiatan.objects.order_by('-tanggal')[:3]
    return render(request, 'main/home.html', {'profil': profil, 'kegiatan': kegiatan_terbaru})

def profil_detail(request):
    profil = Profil.objects.first()
    # Mengambil data Tri Dharma
    penelitian = TriDharma.objects.filter(kategori='PENELITIAN')
    pkm = TriDharma.objects.filter(kategori='PKM')
    publikasi = TriDharma.objects.filter(kategori='PUBLIKASI')
    
    context = {
        'profil': profil,
        'penelitian': penelitian,
        'pkm': pkm,
        'publikasi': publikasi
    }
    return render(request, 'main/profil.html', context)

def materi_kuliah(request):
    matkul_list = MataKuliah.objects.all().prefetch_related('materi')
    return render(request, 'main/materi.html', {'matkul_list': matkul_list})

def video_gallery(request):
    videos = VideoYoutube.objects.all()
    kategori = KategoriVideo.objects.all()
    
    # Filter sederhana via GET parameter
    kat_filter = request.GET.get('kategori')
    if kat_filter:
        videos = videos.filter(kategori__nama=kat_filter)
        
    return render(request, 'main/video.html', {'videos': videos, 'kategori': kategori})

def contact(request):
    profil = Profil.objects.first()
    return render(request, 'main/contact.html', {'profil': profil})

def detail_kegiatan(request, slug):
    # Ambil 1 kegiatan berdasarkan slug, jika tidak ada tampilkan 404
    kegiatan = get_object_or_404(Kegiatan, slug=slug)
    
    # Ambil 5 kegiatan lain untuk sidebar (kecuali yang sedang dibuka)
    kegiatan_lain = Kegiatan.objects.exclude(slug=slug).order_by('-tanggal')[:5]
    
    return render(request, 'main/detail_kegiatan.html', {
        'kegiatan': kegiatan,
        'kegiatan_lain': kegiatan_lain
    })

@login_required
def daftar_absensi(request):
    # mengambil semua kelas yang ada
    kelas_list = Kelas.objects.all().order_by('-semester', 'mata_kuliah__nama')
    return render(request, 'absensi/daftar_kelas.html', {'kelas_list': kelas_list})

@login_required
def input_absensi(request, kelas_id):
    kelas_obj = get_object_or_404(Kelas, id=kelas_id)
    # Ambil mahasiswa yang terdaftar di kelas ini
    siswa_list = kelas_obj.mahasiswa.all().order_by('nim')

    if request.method == "POST":
        topik = request.POST.get('topik')
        tgl = request.POST.get('tanggal')
        pertemuan = request.POST.get('pertemuan_ke')

        # 1. Buat Sesi Baru
        sesi_baru = SesiKuliah.objects.create(
            kelas=kelas_obj, topik=topik, tanggal=tgl, pertemuan_ke=pertemuan
        )

        # 2. Simpan Absensi Massal
        absensi_batch = []
        for siswa in siswa_list:
            status = request.POST.get(f'status_{siswa.id}')
            if status:
                absensi_batch.append(Absensi(sesi=sesi_baru, mahasiswa=siswa, status=status))
        
        Absensi.objects.bulk_create(absensi_batch) # Optimasi query database
        return redirect('daftar_absensi')

    return render(request, 'absensi/input_absensi.html', {
        'kelas': kelas_obj, 'siswa_list': siswa_list, 'today': date.today()
    })