########## Forms de gestion_citas ##########

from django import forms
from django.forms import ModelForm, Textarea, DateInput, TimeInput, Select
from .models import Cita
from gestion_clinica.models import Consultorio

class create_citas_form(forms.ModelForm):

    class Meta:
        model = Cita
        exclude = ['firstupdated', 'lastupdated', 'modifiedby']
        widgets = {
            'appdate': DateInput(attrs={'readonly': 'True'}),
            'apptime': TimeInput(format='%H:%M'),
            'notes': Textarea(attrs={'cols': 38, 'rows': 3})
            }

class create_citas_paciente_form(forms.ModelForm):

    class Meta:
        model = Cita
        exclude = ['firstupdated', 'lastupdated', 'modifiedby']
        widgets = {
            'fk_Paciente': forms.HiddenInput(),
            'appdate': DateInput(attrs={'readonly': 'True'}),
            'apptime': TimeInput(format='%H:%M'),
            'notes': Textarea(attrs={'cols': 38, 'rows': 3})
            }

class edit_citas_form(forms.Form):
    
    # Campos del formulario
    notes = forms.CharField(label = 'Notas', widget = Textarea(attrs={'cols': 18, 'rows': 3}), required = False)