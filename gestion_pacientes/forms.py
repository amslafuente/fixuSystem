from django import forms
from django.forms import ModelForm, Textarea, DateInput, TextInput, NumberInput, EmailInput, Select
from .models import Paciente
from django.conf import settings
from fixuSystem.progvars import selOrder



#########################################
#                                       #
#           FORMS DE PACIENTES          #
#                                       #
#########################################

class create_edit_pacientes_form(forms.ModelForm):

    class Meta:
        model = Paciente
        exclude = ['firstupdated', 'lastupdated', 'modifiedby']
        widgets = {
            'name': TextInput(attrs={'style': 'width: 180px;'}),
            'familyname': TextInput(attrs={'style': 'width: 180px'}),
            'dni': TextInput(attrs={'style': 'width: 120px;'}),
            'birthdate': DateInput(attrs={'style': 'width: 120px'}),
            'sex': Select(attrs={'style': 'width: 180px'}),
            'job': TextInput(attrs={'style': 'width: 180px'}),
            'address': TextInput(attrs={'style': 'width: 410px'}),
            'city': TextInput(attrs={'style': 'width: 180px'}),
            'province': TextInput(attrs={'style': 'width: 180px'}),
            'country': TextInput(attrs={'style': 'width: 180px'}),
            'email': EmailInput(attrs={'style': 'width: 180px'}),
            'postcode': NumberInput(attrs={'style': 'width: 120px', 'min': 0, 'max': 99999}),
            'phone1': NumberInput(attrs={'style': 'width: 120px', 'min': 0, 'max': 999999999}),
            'phone2': NumberInput(attrs={'style': 'width: 120px', 'min': 0, 'max': 999999999}),
            'notifyvia': Select(attrs={'style': 'width: 180px'}),
            'notes': Textarea(attrs={'cols': 76, 'rows': 3})
            }

# Form para seleccionar pacientes para mostrar
class select_pacientes_form(forms.Form):

    dni = forms.CharField(label = 'DNI:', max_length = 10, required = False)
    name = forms.CharField(label = 'Nombre:', max_length = 10, required = False)
    familyname = forms.CharField(label = 'Apellidos:',  max_length = 10, required = False)
    orderby = forms.ChoiceField(label = 'Ordenar por:', choices = selOrder)
    orderby.widget = Select(attrs={'style': 'width: 242px;'}, choices = selOrder)

# Form para seleccionar UN paciente para editar
class select_edit_pacientes_form(forms.Form):

    idpac = forms.CharField(label = 'id Paciente:', max_length = 10, required = False)
    idpac.widget = NumberInput(attrs={'style': 'width: 140px;', 'min': 0, 'max': 9999999999})
    dni = forms.CharField(label = 'DNI Paciente:', max_length = 10, required = False)
    dni.widget = TextInput(attrs={'style': 'width: 140px;', 'maxlength': 10})
    