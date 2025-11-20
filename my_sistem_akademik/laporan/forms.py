from django import forms
from .models import Rapor, SPP, GajiGuru

class RaporForm(forms.ModelForm):
    class Meta:
        model = Rapor
        fields = '__all__'

class SPPForm(forms.ModelForm):
    class Meta:
        model = SPP
        fields = '__all__'

class GajiGuruForm(forms.ModelForm):
    class Meta:
        model = GajiGuru
        fields = '__all__'
