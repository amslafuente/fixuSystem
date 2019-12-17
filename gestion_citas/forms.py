########## Forms de gestion_citas ##########

from django import forms
from django.forms import ModelForm, Textarea, DateInput, TimeInput, Select
from .models import Cita
from gestion_clinica.models import Consultorio

###############################################################################

# Form para crear citas

class create_citas_form(forms.ModelForm):

    # Overrride el ModelChoiceField para poner solo los consultorios disponibles
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fk_Consultorio'] = forms.ModelChoiceField(queryset = Consultorio.objects.filter(officeIsavail = True))

    class Meta:
        model = Cita
        exclude = ['firstupdated', 'lastupdated', 'modifiedby']
        widgets = {
            'appdate': DateInput(attrs={'readonly': 'True'}),
            'apptime': TimeInput(format='%H:%M'),
            'notes': Textarea(attrs={'cols': 40, 'rows': 5})
            }

class create_citas_paciente_form(forms.ModelForm):

    # Overrride el ModelChoiceField para poner solo los consultorios disponibles
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fk_Consultorio'] = forms.ModelChoiceField(queryset = Consultorio.objects.filter(officeIsavail = True))

    class Meta:
        model = Cita
        exclude = ['firstupdated', 'lastupdated', 'modifiedby']
        widgets = {
            'fk_Paciente': forms.HiddenInput(),
            'appdate': DateInput(attrs={'readonly': 'True'}),
            'apptime': TimeInput(format='%H:%M'),
            'notes': Textarea(attrs={'cols': 40, 'rows': 5})
            }

###############################################################################
