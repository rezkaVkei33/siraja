from django import forms
from .models import Terminal, Kios, Angkutan, Rute, Jadwal, Penumpang, Galeri, Saran, Trayek, Kategori
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class TerminalForm(forms.ModelForm):
    class Meta:
        model = Terminal
        fields = '__all__'

class KiosForm(forms.ModelForm):
    class Meta:
        model = Kios
        fields = '__all__'

class AngkutanForm(forms.ModelForm):
    class Meta:
        model = Angkutan
        fields = '__all__'

class RuteForm(forms.ModelForm):
    class Meta:
        model = Rute
        fields = '__all__'

class PenumpangForm(forms.ModelForm):
    class Meta:
        model   = Penumpang
        fields  = '__all__'

class JadwalForm(forms.ModelForm):
    class Meta:
        model   = Jadwal
        fields  = '__all__'

class GaleriForm(forms.ModelForm):
    class Meta:
        model   = Galeri
        fields  = '__all__'

class SaranForm(forms.ModelForm):
    class Meta:
        model   = Saran
        fields = '__all__'

class KategoriForm(forms.ModelForm):
    class Meta:
        model   = Kategori
        fields = '__all__'

class TrayekForm(forms.ModelForm):
    class Meta:
        model   = Trayek
        fields = '__all__'
    