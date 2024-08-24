import pandas as pd
from reportlab.lib import colors
from django.shortcuts import render
from django.http import HttpResponse
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook
from .models import Penumpang, Angkutan, Jadwal, Rute, Kategori, Trayek
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import datetime
from calendar import month_name

@login_required(login_url=settings.LOGIN_URL)
def ekspor_trayek_view(request):
    kategori_list = Kategori.objects.all()
    selected_kategori_id = request.GET.get('selected_kategori_id')

    context = {
        'title': 'Laporan Trayek',
        'kategori_list': kategori_list,
        'selected_kategori_id': selected_kategori_id,
    }
    return render(request, 'laporan/eksport_trayek.html', context)

@login_required(login_url=settings.LOGIN_URL)
def ekspor_trayek(request):
    selected_kategori_id = request.GET.get('selected_kategori_id')
    if selected_kategori_id:
        trayek_list = Trayek.objects.filter(id_kategori_id=selected_kategori_id)
    else:
        trayek_list = Trayek.objects.all()

    combined_data = []
    for trayek in trayek_list:
        combined_data.append({
            'trayek': trayek,
            'rute': trayek.id_rute,
            'kategori': trayek.id_kategori,
        })

    export_type = request.GET.get('type', 'excel')

    if export_type == 'pdf':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=trayek_rute.pdf'

        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []
        styles = getSampleStyleSheet()
        elements.append(Paragraph('Laporan Data Trayek dan Rute', styles['Title']))

        table_data = [['Trayek', 'Jarak (Km)', 'Jumlah Armada', 'Rute Asal', 'Rute Tujuan', 'Kategori']]
        for item in combined_data:
            table_data.append([
                item['trayek'].jenis_trayek,
                item['trayek'].jarak,
                item['trayek'].jumlah_armada,
                item['rute'].asal if item['rute'] else '',
                item['rute'].tujuan if item['rute'] else '',
                item['kategori'].kategori if item['kategori'] else '',
            ])

        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        doc.build(elements)
        return response

    else: 
        df = pd.DataFrame([{
            'Trayek': item['trayek'].jenis_trayek,
            'Jarak (Km)': item['trayek'].jarak,
            'Jumlah Armada': item['trayek'].jumlah_armada,
            'Rute Asal': item['rute'].asal if item['rute'] else '',
            'Rute Tujuan': item['rute'].tujuan if item['rute'] else '',
            'Kategori': item['kategori'].kategori if item['kategori'] else '',
        } for item in combined_data])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=Trayek_rute.xlsx'
        df.to_excel(response, index=False, engine='openpyxl')

    return response

@login_required(login_url=settings.LOGIN_URL)
def ekspor_penumpang_view(request):
    months = range(1, 13)
    years = range(2020, datetime.now().year + 1)

    context = {
        'months': months,
        'years': years,
    }
    
    return render(request, 'laporan/ekspor_penumpang.html', context)

@login_required(login_url=settings.LOGIN_URL)
def ekspor_angkutan_view(request):
    context = {
        'title' : 'Ekspor Data Angkutan'
    }
    return render(request, 'laporan/ekspor_angkutan.html', context)

@login_required(login_url=settings.LOGIN_URL)
def ekspor_penumpang(request):
    month = request.GET.get('month')
    year = request.GET.get('year')

    penumpang_list = Penumpang.objects.filter(
        waktu_berangkat__month=month, 
        waktu_berangkat__year=year
    )

    summary_data = penumpang_list.values(
        'id_angkutan__plat_nomor',
        'id_angkutan__id_rute__asal',
        'id_angkutan__id_rute__tujuan',
        'id_angkutan__nama_sopir'
    ).annotate(
        total_naik=Sum('jumlah_naik'), 
        total_turun=Sum('jumlah_turun')
    ).order_by('id_angkutan__nama_sopir')

    # Konversi ke DataFrame
    df = pd.DataFrame(list(summary_data))

    # Tentukan jenis ekspor
    export_type = request.GET.get('type', 'excel')

    if export_type == 'pdf':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=penumpang_{month}_{year}.pdf'

        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []
        styles = getSampleStyleSheet()

        # Judul Laporan
        elements.append(Paragraph(f'Laporan Penumpang - {month}/{year}', styles['Title']))

        # Tabel data
        table_data = [['Nama Sopir', 'Plat Nomor', 'Asal', 'Tujuan', 'Total Naik', 'Total Turun']]
        for index, row in df.iterrows():
            table_data.append([
                row['id_angkutan__nama_sopir'],
                row['id_angkutan__plat_nomor'],
                row['id_angkutan__id_rute__asal'],
                row['id_angkutan__id_rute__tujuan'],
                str(row['total_naik']),
                str(row['total_turun'])
            ])

        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        doc.build(elements)
        return response

    else:  # Default ke Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=penumpang_{month}_{year}.xlsx'

        # Tambahkan header ke DataFrame
        df.columns = ['Nama Sopir', 'Plat Nomor', 'Asal', 'Tujuan', 'Total Naik', 'Total Turun']

        df.to_excel(response, index=False, engine='openpyxl')
        return response

@login_required(login_url=settings.LOGIN_URL)
def ekspor_angkutan(request):
    angkutan_list = Angkutan.objects.all()
    rute_list = Rute.objects.all()

    
    combined_data = []
    for angkutan in angkutan_list:
        combined_data.append({
            'angkutan': angkutan,
            'rute': angkutan.id_rute,
        })

    
    export_type = request.GET.get('type', 'excel')

    if export_type == 'pdf':
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=angkutan_rute.pdf'

        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []
        styles = getSampleStyleSheet()
        elements.append(Paragraph('Laporan Data Angkutan dan Rute', styles['Title']))

        
        table_data = [['Nama Sopir', 'Plat Nomor', 'Jenis Angkutan', 'Rute Asal', 'Rute Tujuan']]
        for item in combined_data:
            table_data.append([
                item['angkutan'].nama_sopir,
                item['angkutan'].plat_nomor,
                item['angkutan'].jenis_angkutan,
                item['rute'].asal if item['rute'] else '',
                item['rute'].tujuan if item['rute'] else '',
            ])

        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        doc.build(elements)
        return response

    else:  
        df = pd.DataFrame([{
            'Nama Sopir': item['angkutan'].nama_sopir,
            'Plat Nomor': item['angkutan'].plat_nomor,
            'Jenis Angkutan': item['angkutan'].jenis_angkutan,
            'Rute Asal': item['rute'].asal if item['rute'] else '',
            'Rute Tujuan': item['rute'].tujuan if item['rute'] else '',
        } for item in combined_data])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=Angkutan_rute.xlsx'
        df.to_excel(response, index=False, engine='openpyxl')

    return response