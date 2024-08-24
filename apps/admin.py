from django.contrib import admin
from .models import Terminal, Kios, Angkutan, Rute, Jadwal, Penumpang

# Register your models here.
admin.site.register(Terminal)
admin.site.register(Kios)
admin.site.register(Angkutan)
admin.site.register(Rute)
admin.site.register(Jadwal)
admin.site.register(Penumpang)