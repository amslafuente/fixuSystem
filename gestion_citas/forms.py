from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateInput, TimeInput, Select
from .models import Cita
from gestion_clinica.models import Consultorio



#########################################
#                                       #
#    CREACION Y EDICION DE CITAS        #
#                                       #
#########################################

# Creacion de citas sin incluir el paciente
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

# Creacion de citas incluyendo el paciente
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
            'notes': Textarea(attrs={'cols': 32, 'rows': 3})
        }
# Edicion de citas: solo modifica las notas
class edit_citas_form(forms.Form):
    
    notes = forms.CharField(label = 'Notas', widget = Textarea(attrs={'cols': 22, 'rows': 3}), required = False)



#########################################
#                                       #
#          NOTIFICACION DE CITAS        #
#                                       #
#########################################

# Form para eleigir las consiciones para notificar las citas
class customNotifDias_form(forms.Form):
        
    day = forms.IntegerField(required = False)
    day.widget = forms.widgets.NumberInput(attrs={'style': 'width: 50px', 'min': 1, 'max': 99, 'onchange': 'hideButton()'})   
    untilday = forms.BooleanField(required = False)    
    untilday.widget = forms.widgets.CheckboxInput(attrs={'onclick': 'hideButton()'})

# Form para poner el flag de notficada a las citas a notificar por telefono
class setnotified_citas_form(forms.ModelForm):

    class Meta:
        model = Cita
        fields = ['appnotified']

