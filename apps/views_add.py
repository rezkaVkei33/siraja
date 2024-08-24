from django.shortcuts import render, redirect, get_list_or_404
from django.urls import reverse
from django.contrib import messages
from .models import Terminal, Kios, Angkutan, Rute, Jadwal, Penumpang, Galeri, Saran, Kategori, Trayek
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required(login_url=settings.LOGIN_URL)
def tambah_penumpang(request):
    if request.method == 'POST':
        id_angkutan = request.POST['id_angkutan']
        jumlah_naik = request.POST['jumlah_naik']
        jumlah_turun = request.POST['jumlah_turun']
        waktu_berangkat = request.POST['waktu_berangkat']
        angkutan = Angkutan.objects.get(id_angkutan=id_angkutan)
        Penumpang.objects.create(id_angkutan=angkutan, jumlah_naik=jumlah_naik, jumlah_turun=jumlah_turun, waktu_berangkat=waktu_berangkat)
        messages.success(request, 'Data penumpang berhasil ditambahkan.')
        return redirect(reverse('data_penumpang'))
    return render(request, 'penumpang/data_penumpang.html')

@login_required(login_url=settings.LOGIN_URL)
def tambah_terminal(request):
    if request.method == 'POST':
        nama_terminal = request.POST['nama_terminal']
        lokasi = request.POST['lokasi']
        Terminal.objects.create(nama_terminal=nama_terminal,lokasi=lokasi)
        messages.success(request,'Data terminal berhasil ditambahkan')
        return redirect(reverse('data_terminal'))
    return render(request, 'termainal/data_terminal.html')

@login_required(login_url=settings.LOGIN_URL)
def tambah_angkutan(request):
    if request.method == 'POST':
        id_rute = request.POST['id_rute']
        nama_sopir = request.POST['nama_sopir']
        jenis_angkutan = request.POST['jenis_angkutan']
        plat_nomor = request.POST['plat_nomor']
        keterangan = request.POST['keterangan']
        tarif = request.POST['tarif']
        telepon = request.POST['telepon']
        rute = Rute.objects.get(id_rute=id_rute)
        Angkutan.objects.create(
            nama_sopir=nama_sopir,
            jenis_angkutan=jenis_angkutan,
            plat_nomor=plat_nomor,
            keterangan=keterangan,
            id_rute=rute, 
            tarif=tarif,
            telepon=telepon)
        messages.success(request,'Data angkutan berhasil ditambahkan.')
        return redirect(reverse('data_angkutan'))
    return render(request,'angkutan/data_angkutan.html')

@login_required(login_url=settings.LOGIN_URL)
def tambah_rute(request):
    if request.method == 'POST':
        asal = request.POST['asal']
        tujuan =request.POST['tujuan']
        Rute.objects.create(asal=asal,tujuan=tujuan)
        messages.success(request,'Data rute berhasil ditambahkan.')
        return redirect(reverse('data_rute'))
    return render(request, 'rute/data_rute.html')

@login_required(login_url=settings.LOGIN_URL)
def tambah_kios(request):
    if request.method == 'POST':
        id_terminal = request.POST['id_terminal']
        nama_kios = request.POST['nama_kios']
        if id_terminal:
            terminal = Terminal.objects.get(id_terminal=id_terminal)
            Kios.objects.create(id_terminal=terminal, nama_kios=nama_kios)
            messages.success(request, 'Data kios berhasil ditambahkan.')
        else:
            messages.error(request, 'Pilih terminal yang valid.')
        return redirect(reverse('data_kios'))
    return render(request, 'kios/data_kios.html')

def tambah_saran(request):
    if request.method == 'POST':
        nama = request.POST['nama']
        telepon = request.POST['telepon']
        subjek = request.POST['subjek']
        pesan = request.POST['pesan']
        Saran.objects.create(
            nama=nama,
            telepon=telepon,
            subjek=subjek,
            pesan=pesan
        )
        messages.success(request, 'Kotak saran telah dikirim')
        return redirect(reverse('kontak'))
    return render(request, 'kontak.html')

@login_required(login_url=settings.LOGIN_URL)
def tambah_jadwal(request):
    if request.method == 'POST':
        id_angkutan = request.POST['id_angkutan']
        id_terminal = request.POST['id_terminal']
        waktu_berangkat = request.POST['waktu_berangkat']
        jam_masuk = request.POST['jam_masuk']
        jam_keluar = request.POST['jam_keluar']
        
        angkutan = Angkutan.objects.get(id_angkutan=id_angkutan)
        terminal = Terminal.objects.get(id_terminal=id_terminal)
        
        Jadwal.objects.create(
            id_angkutan=angkutan,
            id_terminal=terminal,
            waktu_berangkat=waktu_berangkat,
            jam_masuk=jam_masuk,
            jam_keluar=jam_keluar
        )
        
        messages.success(request, 'Data jadwal berhasil ditambahkan.')
        return redirect(reverse('data_jadwal'))

    angkutan_list = Angkutan.objects.all()
    terminal_list = Terminal.objects.all()

    return render(request, 'jadwal/tambah_jadwal.html', {
        'angkutan_list': angkutan_list,
        'terminal_list': terminal_list
    })

@login_required(login_url=settings.LOGIN_URL)
def tambah_galeri(request):
    if request.method == 'POST':
        judul = request.POST['judul']
        deskripsi = request.POST['deskripsi']
        file_upload = request.FILES['file_upload']

        fs = FileSystemStorage()
        filename = fs.save(file_upload.name, file_upload)

        galeri = Galeri(judul=judul, deskripsi=deskripsi, file_upload=filename)
        galeri.save()
        messages.success(request, 'Galeri berhasil di upload.')
        return redirect('data_galeri')  

    return render(request, 'galeri/tambah_galeri.html')

@login_required(login_url=settings.LOGIN_URL)
def tambah_trayek(request):
    if request.method == 'POST':
        id_kategori = request.POST['id_kategori']
        id_rute     = request.POST['id_rute']
        jenis_trayek = request.POST['jenis_trayek']
        jarak       = request.POST.get('jarak', None)
        jumlah_armada = request.POST.get('jumlah_armada', None)

        # Periksa apakah jarak atau jumlah_armada kosong dan atur menjadi None
        if jarak == '':
            jarak = None
        if jumlah_armada == '':
            jumlah_armada = None

        kategori = Kategori.objects.get(id_kategori=id_kategori)
        rute = Rute.objects.get(id_rute=id_rute)

        Trayek.objects.create(
            id_kategori=kategori,
            id_rute=rute,
            jenis_trayek=jenis_trayek,
            jarak=jarak,
            jumlah_armada=jumlah_armada
        )

        messages.success(request, 'Data trayek berhasil ditambahkan.')
        return redirect(reverse('data_trayek'))
    
    kategori_list = Kategori.objects.all()
    rute_list = Rute.objects.all()

    return render(request, 'trayek/data_trayek',{
        'kategori_list':kategori_list,
        'rute_list':rute_list
    })

@login_required(login_url=settings.LOGIN_URL)
def tambah_kategori(request):
    if request.method == 'POST':
        kategori = request.POST['kategori']
        Kategori.objects.create(kategori=kategori)
        messages.success(request,'Data kategori berhasil ditambahkan.')
        return redirect(reverse('data_trayek'))
    return render(request, 'rute/data_trayek.html')