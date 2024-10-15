from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from .models import Terminal, Kios, Angkutan, Rute, Jadwal, Penumpang, Galeri, Saran, Trayek, Kategori
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import Count, Sum
from datetime import datetime

# Create your views here.
def index(request):
    galeri_list = Galeri.objects.all().order_by('-created_at')

    paginator = Paginator(galeri_list, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        judul = request.POST['judul']
        deskripsi = request.POST['deskripsi']
        file_upload = request.FILES['file_upload'] if 'file_upload' in request.FILES else ''

        galeri = Galeri(judul=judul, deskripsi=deskripsi, file_upload=file_upload)
        galeri.save()
        return redirect('data_galeri')

    contex = {
        'title':'SIRAJA',
        'galeri' : 'Galeri',
        'tentang' : 'Tentang Dishub Beltim',
        'heading':'sistem informasi jadwal angkutan',
        'subheading':'di kelas terbuka',
        'data_galeri': galeri_list,
        'page_obj': page_obj,
    }
    return render(request, 'index.html',contex)

def stk_penumpang(request):
    context = {
        "title" : "Penumpang Naik & Turun"
    }
    return render(request, 'stk_penumpang.html',context)

def trayek(request):
    query = request.GET.get('t')
    trayek_list = Trayek.objects.select_related('id_rute','id_kategori').order_by('-created_at')
    kategori_list = Kategori.objects.all()

    if query:
        trayek_list = trayek_list.filter(
            id_kategori = query
        )
    
    trayek_count = Trayek.objects.count()

    paginator = Paginator(trayek_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    context = {
        'title'     : 'INFORMASI TRAYEK',
        'page_obj' : page_obj,
        'trayek_count' : trayek_count,
        'kategori_list' : kategori_list,
    }

    return render(request, 'trayek.html', context)

def profil(request):
    
    context = {
        'title'   : 'Profil Terminal',
        'struktur'  : 'STRUKTUR ORGANISASI SEKSI ANGKUTAN DALAM PROYEK & TERMINAL',
        'tentang'  : 'TERMINAL MANGGAR',
        'layout'  : 'LAYOUT TERMINAL MANGGAR',
    }
    return render(request, 'profil.html', context)

def galeri(request):
    galeri_list = Galeri.objects.all().order_by('-created_at')
    pagiantor = Paginator(galeri_list,8)
    page_number = request.GET.get('page')
    page_obj = pagiantor.get_page(page_number)
    
    context = {
        'page_obj' : page_obj,
        'title'  : 'Galeri'
    }
    return render(request, 'galeri.html', context)

def kontak(request):
    context = {
        'title' : 'Kontak',
        'saran' : 'KOTAK SARAN',
        'kontak' : 'HUBUNGI KAMI',
    }
    return render(request, 'kontak.html', context)

def jadwal(request):
    query = request.GET.get('j', '')
    jadwal_list = Jadwal.objects.select_related('id_angkutan', 'id_terminal', 'id_angkutan__id_rute')
    jadwal_count = Jadwal.objects.count()
    if query:
        jadwal_list = jadwal_list.filter(
            Q(id_angkutan__nama_sopir__icontains=query) |
            Q(id_angkutan__plat_nomor__icontains=query) |
            Q(id_terminal__nama_terminal__icontains=query) |
            Q(id_terminal__lokasi__icontains=query)
        )

    paginator = Paginator(jadwal_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title' : 'JADWAL KEBERANGKATAN - KEDATANGAN',
        'page_obj': page_obj,
        'query': query,
        'jadwal_count': jadwal_count,
    }
    return render(request, 'jadwal.html', context)

def angkutan(request):
    query = request.GET.get('a', '')
    angkutan_list = Angkutan.objects.select_related('id_rute')
    angkutan_count = Angkutan.objects.count()
    if query:
        angkutan_list = angkutan_list.filter(
            Q(nama_sopir__icontains=query) |
            Q(plat_nomor__icontains=query) |
            Q(jenis_angkutan__icontains=query) |
            Q(id_rute__tujuan__icontains=query)
        )

    paginator = Paginator(angkutan_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title' : 'INFORMASI ANGKUTAN',
        'page_obj': page_obj,
        'query': query,
        'angkutan_count': angkutan_count,
    }
    return render(request, 'angkutan.html', context)

@login_required(login_url=settings.LOGIN_URL)
def penumpang_summary(request):
    
    month = request.GET.get('month')
    year = request.GET.get('year')

    penumpang_list = Penumpang.objects.all()
    if month and year:
        penumpang_list = penumpang_list.filter(
            waktu_berangkat__month=month,
            waktu_berangkat__year=year
        )

    summary_data = penumpang_list.values('id_angkutan__nama_sopir').annotate(
        total_naik=Sum('jumlah_naik'),
        total_turun=Sum('jumlah_turun')
    ).order_by('id_angkutan__nama_sopir')

    month_names = [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]

    context = {
        'title': 'total penumpang naik dan turun',
        'summary_data': summary_data,
        'months': zip(range(1, 13), month_names),
        'years': range(2020, datetime.now().year + 1),
    }
   
    return render(request, 'chart/hitung_angkutan_penumpang.html', context)

@login_required(login_url=settings.LOGIN_URL)
def data_kotak_saran(request):
    query = request.GET.get('s', '')
    saran_list = Saran.objects.all().order_by('-created_at')
    if query:
        saran_list = saran_list.filter(
            Q(nama__icontains=query)
        )
    pagiantor = Paginator(saran_list, 5)
    page_number = request.GET.get('page')
    page_obj = pagiantor.get_page(page_number)
    context = {
        'title' : 'KOTAK SARAN',
        'page_obj' : page_obj,
        'query' : query
    }
    return render(request, 'galeri/data_kotak_saran.html', context)
    
@login_required(login_url=settings.LOGIN_URL)
def base(request):
    contex = {
        'title':'SIRAJA',
        'heading':'sistem informasi jadwal angkutan',
    }
    return render(request, 'base.html',contex)

@login_required(login_url=settings.LOGIN_URL)
def data_penumpang(request):
    query = request.GET.get('q', '')
    month = request.GET.get('month')
    penumpang_list = Penumpang.objects.select_related('id_angkutan', 'id_angkutan__id_rute').order_by('-created_at')
    angkutan_list = Angkutan.objects.all()

    if query:
        penumpang_list = penumpang_list.filter(
            Q(id_angkutan__nama_sopir__icontains=query) |
            Q(id_angkutan__plat_nomor__icontains=query) |
            Q(id_angkutan__jenis_angkutan__icontains=query) |
            Q(id_angkutan__id_rute__asal__icontains=query) |
            Q(id_angkutan__id_rute__tujuan__icontains=query)
        )

    if month:
        year, month = map(int, month.split('-'))
        penumpang_list = penumpang_list.filter(
            waktu_berangkat__year=year,
            waktu_berangkat__month=month
        )

    paginator = Paginator(penumpang_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data_penumpang_angkutan = []

    for penumpang in page_obj:
        data_penumpang_angkutan.append({
            'id_angkutan': penumpang.id_angkutan.id_angkutan if penumpang.id_angkutan else '',
            'plat_nomor': penumpang.id_angkutan.plat_nomor if penumpang.id_angkutan else '',
            'nama_sopir': penumpang.id_angkutan.nama_sopir if penumpang.id_angkutan else '',
            'jenis_angkutan': penumpang.id_angkutan.jenis_angkutan if penumpang.id_angkutan else '',
            'rute_asal': penumpang.id_angkutan.id_rute.asal if penumpang.id_angkutan and penumpang.id_angkutan.id_rute else '',
            'rute_tujuan': penumpang.id_angkutan.id_rute.tujuan if penumpang.id_angkutan and penumpang.id_angkutan.id_rute else '',
            'id_penumpang': penumpang.id_penumpang,
            'jumlah_naik': penumpang.jumlah_naik,
            'jumlah_turun': penumpang.jumlah_turun,
            'waktu_berangkat': penumpang.waktu_berangkat
        })

    context = {
        'data_penumpang_angkutan': data_penumpang_angkutan,
        'angkutan_list': angkutan_list,
        'page_obj': page_obj,
        'query': query,
        'month': request.GET.get('month') 
    }

    return render(request, 'penumpang/data_penumpang.html', context)

@login_required(login_url=settings.LOGIN_URL)
def data_terminal(request):
    terminals = Terminal.objects.all()
    return render(request, 'terminal/data_terminal.html', {'terminals': terminals})

@login_required(login_url=settings.LOGIN_URL)
def data_kios(request):
    query = request.GET.get('k', '')
    kios_list = Kios.objects.select_related('id_terminal').all()
    terminal_list = Terminal.objects.all()
    
    if query:
        kios_list = kios_list.filter(
            Q(nama_kios__icontains=query) |
            Q(id_terminal__nama_terminal__icontains=query)
        )

    paginator = Paginator(kios_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data_kios = []

    for kios in page_obj:
        data_kios.append({
            'id_kios': kios.id_kios,
            'nama_kios': kios.nama_kios,
            'id_terminal': kios.id_terminal.id_terminal if kios.id_terminal else '',
            'nama_terminal': kios.id_terminal.nama_terminal if kios.id_terminal else '',
            'lokasi': kios.id_terminal.lokasi if kios.id_terminal else ''
        })

    context = {
        'data_kios': data_kios,
        'terminals': terminal_list,
        'page_obj': page_obj,
        'query': query
    }
    return render(request, 'kios/data_kios.html', context)

@login_required(login_url=settings.LOGIN_URL)
def data_rute(request):
    query = request.GET.get('r', '')  
    rute_list = Rute.objects.all().order_by('-created_at')

    if query:
        rute_list = rute_list.filter(
            Q(asal__icontains=query) |
            Q(tujuan__icontains=query)
        ).distinct()

    paginator = Paginator(rute_list, 5) 
    page_number = request.GET.get('page', 1)  
    page_obj = paginator.get_page(page_number)
    
    context = {
        'data_rute': page_obj,
        'query': query,
    }


    return render(request, 'rute/data_rute.html', context)


@login_required(login_url=settings.LOGIN_URL)
def data_jadwal(request):
    query = request.GET.get('j', '')
    jadwal_list = Jadwal.objects.select_related('id_angkutan', 'id_terminal').all().order_by('-created_at')
    angkutan_list = Angkutan.objects.all()
    terminal_list = Terminal.objects.all()

    if query:
        jadwal_list = jadwal_list.filter(
            Q(id_angkutan__nama_sopir__icontains=query) |
            Q(id_angkutan__plat_nomor__icontains=query) |
            Q(id_terminal__nama_terminal__icontains=query) |
            Q(id_terminal__lokasi__icontains=query)
        )

    paginator = Paginator(jadwal_list, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data_jadwal = []

    for jadwal in page_obj:
        penumpang_list = Penumpang.objects.filter(id_angkutan=jadwal.id_angkutan)
        penumpang_data = [{
            'id_penumpang': penumpang.id_penumpang,
            'jumlah_naik': penumpang.jumlah_naik,
            'jumlah_turun': penumpang.jumlah_turun
        } for penumpang in penumpang_list]

        data = {
            'plat_nomor': jadwal.id_angkutan.plat_nomor if jadwal.id_angkutan else '',
            'nama_sopir': jadwal.id_angkutan.nama_sopir if jadwal.id_angkutan else '',
            'nama_terminal': jadwal.id_terminal.nama_terminal if jadwal.id_terminal else '',
            'lokasi_terminal': jadwal.id_terminal.lokasi if jadwal.id_terminal else '',
            'id_jadwal': jadwal.id_jadwal,
            'waktu_berangkat': jadwal.waktu_berangkat,
            'jam_masuk': jadwal.jam_masuk,
            'jam_keluar': jadwal.jam_keluar,
            'penumpang': penumpang_data
        }
        data_jadwal.append(data)

    context = {
        'data_jadwal': data_jadwal,
        'angkutan_list': angkutan_list,
        'jadwal_list': jadwal_list,
        'terminal_list': terminal_list,
        'page_obj': page_obj,
        'query': query,
    }

    return render(request, 'jadwal/data_jadwal.html', context)

@login_required(login_url=settings.LOGIN_URL)
def data_angkutan(request):
    query = request.GET.get('q', '')
    angkutan_list = Angkutan.objects.all().order_by('-created_at')
    rute_list = Rute.objects.all()
    
    if query:
        angkutan_list = angkutan_list.filter(
            Q(nama_sopir__icontains=query) |
            Q(plat_nomor__icontains=query) |
            Q(jenis_angkutan__icontains=query) |
            Q(keterangan__icontains=query) |
            Q(id_rute__asal__icontains=query) |
            Q(id_rute__tujuan__icontains=query)
        )

    paginator = Paginator(angkutan_list, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    data_angkutan = []

    for angkutan in page_obj:
        jadwals = Jadwal.objects.filter(id_angkutan=angkutan)
        if jadwals.exists():
            for jadwal in jadwals:
                data_angkutan.append({
                    'id_angkutan': angkutan.id_angkutan,
                    'nama_sopir': angkutan.nama_sopir,
                    'plat_nomor': angkutan.plat_nomor,
                    'jenis_angkutan': angkutan.jenis_angkutan,
                    'keterangan': angkutan.keterangan,
                    'rangka_mesin': angkutan.rangka_mesin,
                    'asal': angkutan.id_rute.asal if angkutan.id_rute else '',
                    'tujuan': angkutan.id_rute.tujuan if angkutan.id_rute else '',
                    'waktu_berangkat': jadwal.waktu_berangkat,
                    'jam_masuk': jadwal.jam_masuk,
                    'jam_keluar': jadwal.jam_keluar,
                    'tarif': angkutan.tarif,
                    'telepon': angkutan.telepon,
                })
        else:
            data_angkutan.append({
                'id_angkutan': angkutan.id_angkutan,
                'nama_sopir': angkutan.nama_sopir,
                'plat_nomor': angkutan.plat_nomor,
                'keterangan': angkutan.keterangan,
                'rangka_mesin': angkutan.rangka_mesin,
                'jenis_angkutan': angkutan.jenis_angkutan,
                'asal': angkutan.id_rute.asal if angkutan.id_rute else '',
                'tujuan': angkutan.id_rute.tujuan if angkutan.id_rute else '',
                'waktu_berangkat': '',
                'jam_masuk': '',
                'jam_keluar': '',
                'tarif': angkutan.tarif,
                'telepon': angkutan.telepon,
            })

    context = {
        'data_angkutan': data_angkutan,
        'rute_list': rute_list,
        'page_obj': page_obj,
        'query': query,
    }

    return render(request, 'angkutan/data_angkutan.html', context)

@login_required(login_url=settings.LOGIN_URL)
def manage_user(request, user_id=''):
    users = User.objects.all().order_by('-id')
    if user_id:
        user = get_object_or_404(User, id=user_id)
    else:
        user = ''
    
    if request.method == 'POST':
        if user:  # Jika user sudah ada, update data
            user.username = request.POST['username']
            user.email = request.POST['email']
            user.save()
            messages.success(request, 'User berhasil diperbarui.')
        else:  # Jika tidak ada user, buat user baru
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'User baru berhasil ditambahkan.')
        return redirect('manage_user')
    
    context = {
        'users': users,
        'edit_user': user
    }
    return render(request, 'user/manage_users.html', context)

@login_required(login_url=settings.LOGIN_URL)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'User berhasil dihapus.')
    return redirect('manage_user')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not '':
            login(request, user)
            messages.success(request, 'Login berhasil: Selamat datang di Halaman Admin.')
            return redirect('chart')
        else:
            messages.error(request, 'Login gagal: Username atau password salah.')
            return redirect('index')
    return render(request, 'index.html')

@login_required(login_url=settings.LOGIN_URL)
def chart(request):
    angkutan_count = Angkutan.objects.count()
    kios_count = Kios.objects.count()
    terminal_count = Terminal.objects.count()
    penumpang_count = Penumpang.objects.count()

    total_naik = Penumpang.objects.aggregate(total_naik=Sum('jumlah_naik'))['total_naik'] or 0
    total_turun = Penumpang.objects.aggregate(total_turun=Sum('jumlah_turun'))['total_turun'] or 0

    context = {
        'angkutan_count': angkutan_count,
        'penumpang_count': penumpang_count,
        'kios_count': kios_count,
        'terminal_count': terminal_count,
        'total_naik': total_naik,
        'total_turun': total_turun,
    }

    return render(request, 'chart.html', context)

@login_required(login_url=settings.LOGIN_URL)
def get_chart_data(request):
    # jumlah angkutan berdasarkan jenis angkutan
    angkutan_data = Angkutan.objects.values('jenis_angkutan').annotate(count=Count('id_angkutan'))
    jenis_angkutan = [angkutan['jenis_angkutan'] for angkutan in angkutan_data]
    angkutan_counts = [angkutan['count'] for angkutan in angkutan_data]

    # jumlah penumpang berdasarkan nama sopir
    penumpang_by_sopir = Angkutan.objects.annotate(
        total_naik=Sum('penumpang__jumlah_naik'),
        total_turun=Sum('penumpang__jumlah_turun')
    )

    nama_sopir = [angkutan.nama_sopir for angkutan in penumpang_by_sopir]
    penumpang_naik = [angkutan.total_naik or 0 for angkutan in penumpang_by_sopir]
    penumpang_turun = [angkutan.total_turun or 0 for angkutan in penumpang_by_sopir]

    data = {
        'jenis_angkutan': jenis_angkutan,
        'angkutan_counts': angkutan_counts,
        'nama_sopir': nama_sopir,
        'penumpang_naik': penumpang_naik,
        'penumpang_turun': penumpang_turun,
    }

    return JsonResponse(data)

@login_required(login_url=settings.LOGIN_URL)
def data_galeri(request):
    query = request.GET.get('q', '')  
    galeri_list = Galeri.objects.all().order_by('-created_at')

    if query:
        galeri_list = galeri_list.filter(Q(judul__icontains=query))

    paginator = Paginator(galeri_list, 4) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'data_galeri': page_obj,
        'query': query,
    }
    return render(request, 'galeri/data_galeri.html', context)

@login_required(login_url=settings.LOGIN_URL)
def data_trayek(request):
    query = request.GET.get('t')
    trayek_list = Trayek.objects.select_related('id_rute','id_kategori').order_by('-created_at')
    rute_list = Rute.objects.all()
    kategori_list = Kategori.objects.all()

    if query:
        trayek_list = trayek_list.filter(
            id_kategori = query
        )

    paginator = Paginator(trayek_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    context = {
        'title'     : 'DATA TRAYEK',
        'rute_list' : rute_list,
        'kategori_list' : kategori_list,
        'page_obj' : page_obj,
    }

    return render(request, 'trayek/data_trayek.html', context)