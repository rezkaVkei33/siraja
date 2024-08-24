from django.db import models
from django.utils import timezone
# Create your models here.

class Terminal(models.Model):
    id_terminal     = models.AutoField(primary_key=True)
    nama_terminal   = models.CharField(max_length=255, blank=True, null=True)
    lokasi          = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
       return self.nama_terminal

class Kios(models.Model):
    id_kios     = models.AutoField(primary_key=True)
    id_terminal = models.ForeignKey(Terminal, on_delete=models.SET_NULL, null=True)
    nama_kios   = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nama_kios

class Rute(models.Model):
    id_rute = models.AutoField(primary_key=True)
    asal    = models.CharField(max_length=255, blank=True, null=True)
    tujuan  = models.CharField(max_length=255, blank=True, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id_rute
    
    
class Angkutan(models.Model):
    id_angkutan     = models.AutoField(primary_key=True)
    id_rute         = models.ForeignKey(Rute, on_delete=models.SET_NULL, null=True)
    nama_sopir      = models.CharField(max_length=255, blank=True, null=True)
    plat_nomor      = models.CharField(max_length=255, blank=True, null=True)
    jenis_angkutan  = models.CharField(max_length=255, blank=True, null=True)
    keterangan      = models.TextField(blank=True, null=True)
    tarif           = models.CharField(max_length=255, blank=True, null=True)
    telepon         = models.CharField(max_length=255, blank=True, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama_sopir
    
class Kategori(models.Model):
    id_kategori = models.AutoField(primary_key=True)
    kategori = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.id_kategori} - {self.kategori}"

class Trayek(models.Model):
    id_trayek       = models.AutoField(primary_key=True)
    id_rute         = models.ForeignKey(Rute, on_delete=models.SET_NULL, null=True)
    id_kategori     = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True)
    jenis_trayek    = models.CharField(max_length=255, blank=True, null=True)
    jarak           = models.IntegerField(blank=True, null=True)
    jumlah_armada   = models.IntegerField(blank=True, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id_trayek} - {self.id_rute} - {self.id_kategori} - {self.jenis_trayek}"

class Penumpang(models.Model):
    id_penumpang = models.AutoField(primary_key=True)
    id_angkutan  = models.ForeignKey(Angkutan, on_delete=models.SET_NULL, null=True)
    jumlah_naik  = models.IntegerField(blank=True, null=True)
    jumlah_turun = models.IntegerField(blank=True, null=True)
    waktu_berangkat = models.DateField(blank=True, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_penumpang} - {self.id_angkutan}"
    
class Jadwal(models.Model):
    id_jadwal       = models.AutoField(primary_key=True)
    id_terminal     = models.ForeignKey(Terminal, on_delete=models.SET_NULL, null=True)
    id_angkutan     = models.ForeignKey(Angkutan, on_delete=models.SET_NULL, null=True)
    waktu_berangkat = models.DateField(blank=True, null=True)
    jam_masuk       = models.TimeField(blank=True, null=True)
    jam_keluar      = models.TimeField(blank=True, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.id_angkutan} - {self.id_rute} - {self.waktu_berangkat}"
    
class Galeri(models.Model):
    id_galeri   = models.AutoField(primary_key=True)
    judul       = models.CharField(max_length=255, blank=True, null=True)
    deskripsi   = models.TextField(blank=True, null=True)
    file_upload = models.ImageField(upload_to='galeri/', blank=True, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.id_galeri} - {self.judul}"
    
class Saran(models.Model):
    id_saran = models.AutoField(primary_key=True)
    nama    = models.CharField(max_length=255, blank=True, null=True)
    telepon = models.IntegerField(blank=True, null=True)
    subjek  = models.CharField(max_length=255, blank=True, null=True)
    pesan   = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id_saran} - {self.nama}"