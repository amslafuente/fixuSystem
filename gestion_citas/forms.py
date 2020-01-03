from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateInput, TimeInput, Select
from .models import Cita
from gestion_clinica.models import Consultorio

class create_citas_form(forms.ModelForm):

    class Meta:
        model = Cita
        exclude = ['firstupdated', 'lastupdated', 'modifiedby']
        widgets = {
            'appdate': DateInput(attrs={'readonly': 'True'}),
            'apptime': TimeInput(format='%H:%M'),
            'fk_Paciente': Select(attrs={'style': 'width: 244px;'}),
            'fk_Profesional': Select(attrs={'style': 'width: 244px;'}),
            'fk_Consultorio': Select(attrs={'style': 'width: 244px;'}),
            'status': Select(attrs={'style': 'width: 1px; visibility: hidden;'}),
            'notes': Textarea(attrs={'cols': 32, 'rows': 3})
            }

class create_citas_paciente_form(forms.ModelForm):

    class Meta:
        model = Cita
        exclude = ['firstupdated', 'lastupdated', 'modifiedby']
        widgets = {
            'appdate': DateInput(attrs={'readonly': 'True'}),
            'apptime': TimeInput(format='%H:%M'),
            'fk_Paciente': forms.HiddenInput(),
            'fk_Profesional': Select(attrs={'style': 'width: 244px;'}),
            'fk_Consultorio': Select(attrs={'style': 'width: 244px;'}),
            'status': Select(attrs={'style': 'width: 1px; visibility: hidden;'}),
            'notes': Textarea(attrs={'cols': 32, 'rows': 3})            }

class edit_citas_form(forms.Form):
    
    # Campos del formulario
    notes = forms.CharField(label = 'Notas', widget = Textarea(attrs={'cols': 22, 'rows': 3}), required = False)

# Form para poner el flag de notficada a las citas a notificar por telefono
class setnotified_citas_form(forms.ModelForm):

    class Meta:
        model = Cita
        fields = ['appnotified']