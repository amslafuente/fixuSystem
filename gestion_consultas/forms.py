########## Forms de gestion_consultas ##########

from django import forms
from django.forms import ModelForm
from .models import Consulta
from django.forms import ModelForm, Textarea, DateInput

# Form para crear pacientes

class create_consultas_form(forms.ModelForm):

     class Meta:
        model = Consulta
        exclude = ['firstupdated', 'lastupdated', 'modifiedby']
        widgets = {
            'notes': Textarea(attrs={'cols': 80, 'rows': 5})
            }

