from django import forms
from django.forms import ModelForm, Textarea, DateInput, TextInput, NumberInput, EmailInput, Select
from .models import Paciente
from django.conf import settings
from fixuSystem.progvars import selOrder

# Form para crear pacientes
class create_pacientes_form(forms.ModelForm):

    class Meta:
        model = Paciente
        exclude = ['firstupdated', 'lastupdated', 'modifiedby']
        widgets = {
            'name': TextInput(attrs={'style': 'width: 140px;'}),
            'familyname': TextInput(attrs={'style': 'width: 160px'}),
            'dni': TextInput(attrs={'style': 'width: 120px;'}),
            'birthdate': TextInput(attrs={'style': 'width: 120px'}),
            'sex': Select(attrs={'style': 'width: 140px'}),
            'job': TextInput(attrs={'style': 'width: 160px'}),
            'address': TextInput(attrs={'style': 'width: 240px'}),
            'city': TextInput(attrs={'style': 'width: 160px'}),
            'province': TextInput(attrs={'style': 'width: 120px'}),
            'country': Select(attrs={'style': 'width: 320px'}),
            'email': EmailInput(attrs={'style': 'width: 120px'}),
            'postcode': NumberInput(attrs={'style': 'width: 100px', 'min': 0, 'max': 99999}),
            'phone1': NumberInput(attrs={'style': 'width: 120px', 'min': 0, 'max': 999999999}),
            'phone2': NumberInput(attrs={'style': 'width: 120px', 'min': 0, 'max': 999999999}),
            'notifyvia': Select(attrs={'style': 'width: 120px'}),
            'notes': Textarea(attrs={'cols': 60, 'rows': 5})
            }

# Form para seleccionar pacientes para mostrar
class select_pacientes_form(forms.Form):

    # Campos del formulario
    dni = forms.CharField(label = 'DNI:', max_length = 10, required = False)
    name = forms.CharField(label = 'Nombre:', max_length = 10, required = False)
    familyname = forms.CharField(label = 'Apellidos:',  max_length = 10, required = False)
    orderby = forms.ChoiceField(label = 'Ordenar por:', choices = selOrder)
    orderby.widget = Select(attrs={'style': 'width: 242px;'}, choices = selOrder)

# Form para seleccionar UN paciente para editar
class edit_pacientes_form(forms.Form):

    # Campos del formulario
    idpaciente = forms.CharField(label = 'id Paciente:', max_length = 10, required = False)
    dni = forms.CharField(label = 'DNI Paciente:', max_length = 10, required = False)

# Form para editar pacientes
class edit_id_pacientes_form(forms.ModelForm):

    class Meta:
        model = Paciente
        exclude = ['idPaciente', 'dni', 'firstupdated', 'lastupdated']
        widgets = {
            'name': TextInput(attrs={'style': 'width: 240px;'}),
            'familyname': TextInput(attrs={'style': 'width: 340px'}),
            'birthdate': TextInput(attrs={'style': 'width: 120px'}),
            'sex': Select(attrs={'style': 'width: 140px'}),
            'job': TextInput(attrs={'style': 'width: 202px'}),
            'address': TextInput(attrs={'style': 'width: 360px'}),
            'city': TextInput(attrs={'style': 'width: 200px'}),
            'postcode': NumberInput(attrs={'style': 'width: 80px', 'min': 0, 'max': 99999}),
            'province': TextInput(attrs={'style': 'width: 120px'}),
            'country': Select(attrs={'style': 'width: 275px'}),
            'email': EmailInput(attrs={'style': 'width: 200px'}),
            'phone1': NumberInput(attrs={'style': 'width: 120px', 'min': 0, 'max': 999999999}),
            'phone2': NumberInput(attrs={'style': 'width: 120px', 'min': 0, 'max': 999999999}),
            'notifyvia': Select(attrs={'style': 'width: 120px'}),
            'notes': Textarea(attrs={'cols': 70, 'rows': 3})
            }
