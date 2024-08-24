from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Penumpang
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, TruncYear


def chart_penumpang_pertahun(request):
    context = {
        "title" : "Penumpang Pertahun"
    }
    return render(request, 'chart/penumpang_pertahun.html',context)


def api_penumpang_pertahun(request):
    penumpang_pertahun = Penumpang.objects.annotate(
        tahun=TruncYear('waktu_berangkat')
    ).values('tahun').annotate(
        total_naik=Sum('jumlah_naik'),
        total_turun=Sum('jumlah_turun')
    ).order_by('tahun')

    data = {
        'tahun_labels': [data['tahun'].year for data in penumpang_pertahun],
        'jumlah_naik': [data['total_naik'] for data in penumpang_pertahun],
        'jumlah_turun': [data['total_turun'] for data in penumpang_pertahun],
    }

    return JsonResponse(data)

@login_required(login_url=settings.LOGIN_URL)
def chart_penumpang_perbulan(request):

    context = {
        "title": "Penumpang Perbulan",
        
    }
    return render(request, 'chart/penumpang_perbulan.html', context)

@login_required(login_url=settings.LOGIN_URL)
def api_penumpang_perbulan(request):
    penumpang_perbulan = Penumpang.objects.annotate(
        bulan=TruncMonth('waktu_berangkat')
    ).values('bulan').annotate(
        total_naik=Sum('jumlah_naik'),
        total_turun=Sum('jumlah_turun')
    ).order_by('bulan')

    data = {
        'bulan_labels': [data['bulan'].strftime('%b %Y') for data in penumpang_perbulan],
        'jumlah_naik': [data['total_naik'] for data in penumpang_perbulan],
        'jumlah_turun': [data['total_turun'] for data in penumpang_perbulan],
    }

    return JsonResponse(data)
