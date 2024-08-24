from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Kios, Terminal, Angkutan, Rute, Jadwal, Penumpang, Galeri, Saran, Trayek, Kategori

@login_required(login_url=settings.LOGIN_URL)
def hapus_kios(request, id_kios):
    kios = get_object_or_404(Kios, id_kios=id_kios)
    kios.delete()
    messages.success(request, 'Data kios berhasil dihapus.')
    return redirect(reverse('data_kios'))

@login_required(login_url=settings.LOGIN_URL)
def hapus_terminal(request, id_terminal):
    terminal = get_object_or_404(Terminal, id_terminal=id_terminal)
    terminal.delete()
    messages.success(request, 'Data berhasil dihapus.')
    return redirect(reverse('data_terminal'))

@login_required(login_url=settings.LOGIN_URL)
def hapus_angkutan(request, id_angkutan):
    angkutan = get_object_or_404(Angkutan, id_angkutan=id_angkutan)
    angkutan.delete()
    messages.success(request, 'Data angkutan berhasil dihapus.')
    return redirect(reverse('data_angkutan'))

@login_required(login_url=settings.LOGIN_URL)
def hapus_rute(request, id_rute):
    rute = get_object_or_404(Rute, id_rute=id_rute)
    rute.delete()
    messages.success(request, 'Data rute berhasil dihapus.')
    return redirect(reverse('data_rute'))

@login_required(login_url=settings.LOGIN_URL)
def hapus_jadwal(request, id_jadwal):
    jadwal = get_object_or_404(Jadwal, id_jadwal=id_jadwal)
    jadwal.delete()
    messages.success(request, 'Data jadwal berhasil dihapus.')
    return redirect(reverse('data_jadwal'))

@login_required(login_url=settings.LOGIN_URL)
def hapus_penumpang(request, id_penumpang):
    penumpang = get_object_or_404(Penumpang, id_penumpang=id_penumpang)
    penumpang.delete()
    messages.success(request, 'Data penumpang berhasil dihapus.')
    return redirect(reverse('data_penumpang'))

@login_required(login_url=settings.LOGIN_URL)
def hapus_galeri(request, id_galeri):
    galeri = get_object_or_404(Galeri, id_galeri=id_galeri)
    galeri.delete()
    messages.success(request, 'Data galeri berhasil dihapus.')
    return redirect(reverse('data_galeri'))

@login_required(login_url=settings.LOGIN_URL)
def hapus_saran(request, id_saran):
    saran = get_object_or_404(Saran, id_saran=id_saran)
    saran.delete()
    messages.success(request, 'Data saran berhasil dihapus.')
    return redirect(reverse('data_kotak_saran'))

@login_required(login_url=settings.LOGIN_URL)
def hapus_trayek(request, id_trayek):
    trayek = get_object_or_404(Trayek, id_trayek=id_trayek)
    trayek.delete()
    messages.success(request, 'Data trayek berhasil dihapus.')
    return redirect(reverse('data_trayek'))

@login_required(login_url=settings.LOGIN_URL)
def hapus_kategori(request, id_kategori):
    kategori = get_object_or_404(Kategori, id_kategori=id_kategori)
    kategori.delete()
    messages.success(request, 'Data kategori berhasil dihapus.')
    return redirect(reverse('data_trayek'))

