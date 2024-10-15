import os
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Angkutan, Rute, Penumpang, Kios, Terminal, Jadwal, Galeri, Trayek, Kategori
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse


@login_required(login_url=settings.LOGIN_URL)
def ubah_angkutan(request, id_angkutan):
    angkutan = get_object_or_404(Angkutan, pk=id_angkutan)
    
    if request.method == "POST":
        nama_sopir = request.POST.get('nama_sopir')
        jenis_angkutan = request.POST.get('jenis_angkutan')
        plat_nomor = request.POST.get('plat_nomor')
        keterangan = request.POST.get('keterangan')
        rangka_mesin = request.POST.get('rangka_mesin')
        tarif = request.POST.get('tarif')
        telepon = request.POST.get('telepon')
        id_rute = request.POST.get('id_rute')
        
        angkutan.nama_sopir = nama_sopir
        angkutan.jenis_angkutan = jenis_angkutan
        angkutan.plat_nomor = plat_nomor
        angkutan.keterangan = keterangan
        angkutan.rangka_mesin = rangka_mesin
        angkutan.tarif = tarif
        angkutan.telepon = telepon
        angkutan.id_rute = Rute.objects.get(pk=id_rute)
        messages.success(request, 'Data berhasil diubah.')
        angkutan.save()

        return redirect('data_angkutan')
    
    return HttpResponse(status=405)

@login_required(login_url=settings.LOGIN_URL)
def ubah_penumpang(request, id_penumpang):
    penumpang = get_object_or_404(Penumpang, pk=id_penumpang)

    if request.method == 'POST':
        id_angkutan = request.POST.get('id_angkutan')
        jumlah_naik = request.POST.get('jumlah_naik')
        jumlah_turun = request.POST.get('jumlah_turun')
        waktu_berangkat = request.POST.get('waktu_berangkat')

        penumpang.jumlah_naik = jumlah_naik
        penumpang.jumlah_turun = jumlah_turun
        penumpang.waktu_berangkat = waktu_berangkat
        penumpang.id_angkutan = Angkutan.objects.get(pk=id_angkutan)
        messages.success(request, 'Data berhasil diubah.')
        penumpang.save()

        return redirect('data_penumpang')
    return HttpResponse(status=405)

@login_required(login_url=settings.LOGIN_URL)
def ubah_kios(request, id_kios):
    kios = get_object_or_404(Kios, pk=id_kios)

    if request.method == 'POST':
        id_terminal = request.POST.get('id_terminal')
        nama_kios = request.POST.get('nama_kios')

        kios.nama_kios = nama_kios
        kios.id_terminal = Terminal.objects.get(pk=id_terminal)
        messages.success(request, 'Data berhasil diubah.')
        kios.save()

        return redirect('data_kios')
    return HttpResponse(status=405)

@login_required(login_url=settings.LOGIN_URL)
def ubah_terminal(request, id_terminal):
    terminal = get_object_or_404(Terminal, pk=id_terminal)

    if request.method == 'POST':
        id_terminal = request.POST.get('id_terminal')
        nama_terminal = request.POST.get('nama_terminal')
        lokasi = request.POST.get('lokasi')

        terminal.nama_terminal = nama_terminal
        terminal.lokasi = lokasi
        messages.success(request, 'Data berhasil diubah.')
        terminal.save()

        return redirect('data_terminal')
    return HttpResponse(status=405)

@login_required(login_url=settings.LOGIN_URL)
def ubah_rute(request, id_rute):
    rute = get_object_or_404(Rute, pk=id_rute)

    if request.method == 'POST':
        id_rute = request.POST.get('id_rute')
        asal = request.POST.get('asal')
        tujuan = request.POST.get('tujuan')

        rute.asal = asal
        rute.tujuan = tujuan
        messages.success(request, 'Data berhasil diubah.')
        rute.save()

        return redirect('data_rute')
    return HttpResponse(status=405)

@login_required(login_url=settings.LOGIN_URL)
def ubah_jadwal(request, id_jadwal):
    jadwal = get_object_or_404(Jadwal, pk=id_jadwal)

    if request.method == 'POST':
        id_angkutan = request.POST.get('id_angkutan')
        id_terminal = request.POST.get('id_terminal')
        waktu_berangkat = request.POST.get('waktu_berangkat')
        jam_masuk = request.POST.get('jam_masuk')
        jam_keluar = request.POST.get('jam_keluar')

        jadwal.waktu_berangkat = waktu_berangkat
        jadwal.jam_masuk = jam_masuk
        jadwal.jam_keluar = jam_keluar
        jadwal.id_angkutan = Angkutan.objects.get(pk=id_angkutan)
        jadwal.id_terminal = Terminal.objects.get(pk=id_terminal)
        messages.success(request, 'Data berhasil diubah.')
        jadwal.save()

        return redirect('data_jadwal')
    return HttpResponse(status=405)

@login_required(login_url=settings.LOGIN_URL)
def ubah_galeri(request, id_galeri):
    galeri = get_object_or_404(Galeri, id_galeri=id_galeri)

    if request.method == 'POST':
        galeri.judul = request.POST.get('judul')
        galeri.deskripsi = request.POST.get('deskripsi')

        if 'file_upload' in request.FILES:
            file = request.FILES['file_upload']
            fs = FileSystemStorage()

            # Hapus file lama
            if galeri.file_upload:
                old_file_path = galeri.file_upload.path
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

            # Simpan file baru
            filename = fs.save(file.name, file)
            galeri.file_upload = filename

        galeri.save()
        return redirect('data_galeri') 

    context = {
        'data': galeri
    }
    return render(request, 'galeri/ubah_galeri.html', context)

@login_required(login_url=settings.LOGIN_URL)
def ubah_trayek(request, id_trayek):
    trayek = Trayek.objects.get(id_trayek=id_trayek)
    
    if request.method == 'POST':
        id_kategori = request.POST['id_kategori']
        id_rute = request.POST['id_rute']
        jenis_trayek = request.POST['jenis_trayek']
        jarak = request.POST.get('jarak', None)
        jumlah_armada = request.POST.get('jumlah_armada', None)

        if jarak == '':
            jarak = None
        if jumlah_armada == '':
            jumlah_armada = None

        kategori = Kategori.objects.get(id_kategori=id_kategori)
        rute = Rute.objects.get(id_rute=id_rute)

        trayek.id_kategori = kategori
        trayek.id_rute = rute
        trayek.jenis_trayek = jenis_trayek
        trayek.jarak = jarak
        trayek.jumlah_armada = jumlah_armada
        trayek.save()

        messages.success(request, 'Data trayek berhasil diperbarui.')
        return redirect(reverse('data_trayek'))
    
    kategori_list = Kategori.objects.all()
    rute_list = Rute.objects.all()

    return render(request, 'trayek/edit_trayek.html', {
        'trayek': trayek,
        'kategori_list': kategori_list,
        'rute_list': rute_list
    })

@login_required(login_url=settings.LOGIN_URL)
def ubah_kategori(request, id_kategori):
    data_kategori = get_object_or_404(Kategori, pk=id_kategori)

    if request.method == 'POST':
        kategori = request.POST.get('kategori')

        data_kategori.kategori = kategori
        data_kategori.save()

        messages.success(request, 'Data kategori berhasil diubah.')
        return redirect('data_trayek')

    return HttpResponse(status=405) 