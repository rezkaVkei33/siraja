from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views, views_add, views_delete, views_export, views_update, views_chart
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('chart/', views.chart, name='chart'),
    path('api/chart-data/', views.get_chart_data, name='get_chart_data'),
    path('base/', views.base, name='base'),
    path('login/', views.login_view, name='login'),
    path('manage-user/', views.manage_user, name='manage_user'),
    path('manage-user/<int:user_id>/', views.manage_user, name='manage_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('data_penumpang/', views.data_penumpang, name='data_penumpang'),
    path('tambah_penumpang/', views_add.tambah_penumpang, name='tambah_penumpang'),
    path('hapus_penumpang/<int:id_penumpang>/', views_delete.hapus_penumpang, name='hapus_penumpang'),
    path('ubah_penumpang/<int:id_penumpang>/', views_update.ubah_penumpang, name='ubah_penumpang'),
    path('data_angkutan/', views.data_angkutan, name='data_angkutan'),
    path('tambah_angkutan/', views_add.tambah_angkutan, name='tambah_angkutan'),
    path('hapus_angkutan/<int:id_angkutan>/', views_delete.hapus_angkutan, name='hapus_angkutan'),
    path('ubah_angkutan/<int:id_angkutan>/', views_update.ubah_angkutan, name='ubah_angkutan'),
    path('data_rute/', views.data_rute, name='data_rute'),
    path('tambah_rute/', views_add.tambah_rute, name='tambah_rute'),
    path('hapus_rute/<int:id_rute>/', views_delete.hapus_rute, name='hapus_rute'),
    path('ubah_rute/<int:id_rute>/', views_update.ubah_rute, name='ubah_rute'),
    path('data_jadwal/', views.data_jadwal, name='data_jadwal'),
    path('tambah_jadwal/', views_add.tambah_jadwal, name='tambah_jadwal'),
    path('hapus_jadwal/<int:id_jadwal>/', views_delete.hapus_jadwal, name='hapus_jadwal'),
    path('ubah_jadwal/<int:id_jadwal>/', views_update.ubah_jadwal, name='ubah_jadwal'),
    path('data_terminal/', views.data_terminal, name='data_terminal'),
    path('tambah_terminal/', views_add.tambah_terminal, name='tambah_terminal'),
    path('hapus_terminal/<int:id_terminal>/', views_delete.hapus_terminal, name='hapus_terminal'),
    path('ubah_terminal/<int:id_terminal>/', views_update.ubah_terminal, name='ubah_terminal'),
    path('data_kios/', views.data_kios, name='data_kios'),
    path('tambah_kios/', views_add.tambah_kios, name='tambah_kios'),
    path('hapus_kios/<int:id_kios>/', views_delete.hapus_kios, name='hapus_kios'),
    path('ubah_kios/<int:id_kios>/', views_update.ubah_kios, name='ubah_kios'),
    path('trayek/ekspor/', views_export.ekspor_trayek_view, name='ekspor_trayek_view'),
    path('trayek/ekspor_trayek/', views_export.ekspor_trayek, name='ekspor_trayek'),
    path('penumpang/ekspor/', views_export.ekspor_penumpang_view, name='ekspor_penumpang_view'),
    path('penumpang/ekspor_data/', views_export.ekspor_penumpang, name='ekspor_penumpang'),
    path('angkutan/ekspor/', views_export.ekspor_angkutan_view, name='ekspor_angkutan_view'),
    path('angkutan/ekspor_data/', views_export.ekspor_angkutan, name='ekspor_angkutan'),
    path('penumpang-perbulan/', views_chart.chart_penumpang_perbulan, name='penumpang_perbulan'),
    path('api/penumpang-perbulan/', views_chart.api_penumpang_perbulan, name='api_penumpang_perbulan'),
    path('penumpang-pertahun/', views_chart.chart_penumpang_pertahun, name='penumpang_pertahun'),
    path('api/penumpang-pertahun/', views_chart.api_penumpang_pertahun, name='api_penumpang_perbulan'),
    path('stk_penumpang/', views.stk_penumpang, name='stk_penumpang'),
    path('data_galeri/', views.data_galeri, name='data_galeri'),
    path('galeri/tambah/', views_add.tambah_galeri, name='tambah_galeri'),
    path('galeri/ubah/<int:id_galeri>/', views_update.ubah_galeri, name='ubah_galeri'),
    path('hapus_galeri/<int:id_galeri>/', views_delete.hapus_galeri, name='hapus_galeri'),
    path('profil/', views.profil, name='profil'),
    path('galeri/', views.galeri, name='galeri'),
    path('jadwal/', views.jadwal, name='jadwal'),
    path('trayek/', views.trayek, name='trayek'),
    path('angkutan/', views.angkutan, name='angkutan'),
    path('kontak/', views.kontak, name='kontak'),
    path('tambah_saran/', views_add.tambah_saran, name='tambah_saran'),
    path('data_kotak_saran/', views.data_kotak_saran, name='data_kotak_saran'),
    path('hapus_saran/<int:id_saran>/', views_delete.hapus_saran, name='hapus_saran'),
    path('data_trayek/', views.data_trayek, name='data_trayek'),
    path('tambah_kategori/', views_add.tambah_kategori, name='tambah_kategori'),
    path('ubah_kategori/<int:id_kategori>/', views_update.ubah_kategori, name='ubah_kategori'),
    path('hapus_kategori/<int:id_kategori>/', views_delete.hapus_kategori, name='hapus_kategori'),
    path('tambah_trayek/', views_add.tambah_trayek, name='tambah_trayek'),
    path('ubah_trayek/<int:id_trayek>/', views_update.ubah_trayek, name='ubah_trayek'),
    path('hapus_trayek/<int:id_trayek>/', views_delete.hapus_trayek, name='hapus_trayek'),
    path('penumpang/summary/', views.penumpang_summary, name='penumpang_summary'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)