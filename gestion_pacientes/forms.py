########## Forms de gestion_pacientes ##########

from django import forms
from django.forms import ModelForm, Textarea, DateInput, TextInput, NumberInput, EmailInput, Select
from .models import Paciente
from django.conf import settings
from fixuSystem.progvars import selOrder

class create_pacientes_form(forms.ModelForm):

    class Meta:
        model = Paciente
        exclude = ['firstupdated', 'lastupdated', 'modifiedby']
        widgets = {
            # Texto
            'name': TextInput(attrs={'style': 'width: 300px;'}),
            'familyname': TextInput(attrs={'style': 'width: 300px'}),
            'dni': TextInput(attrs={'style': 'width: 300px;'}),
            'birthdate': TextInput(attrs={'style': 'width: 300px'}),
            'job': TextInput(attrs={'style': 'width: 300px'}),
            'address': TextInput(attrs={'style': 'width: 330px'}),
            'city': TextInput(attrs={'style': 'width: 330px'}),
            'province': TextInput(attrs={'style': 'width: 330px'}),
            # Email
            'email': EmailInput(attrs={'style': 'width: 200px'}),
            # Numeros
            'postcode': NumberInput(attrs={'style': 'width: 330px', 'min': 0, 'max': 99999}),
            'phone1': NumberInput(attrs={'style': 'width: 200px', 'min': 0, 'max': 999999999}),
            'phone2': NumberInput(attrs={'style': 'width: 200px', 'min': 0, 'max': 999999999}),
            # Bloques de texto
            'notes': Textarea(attrs={'cols': 88, 'rows': 5})
            }

# Form para seleccionar pacientes para mostrar

class select_pacientes_form(forms.Form):

    # Campos del formulario
    dni = forms.CharField(label = 'DNI:', max_length = 10, required = False)
    name = forms.CharField(label = 'Nombre:', max_length = 25, required = False)
    familyname = forms.CharField(label = 'Apellidos:', max_length = 50, required = False)
    orderby = forms.ChoiceField(label = 'Ordenar por:', choices = selOrder)

# Form para seleccionar UN paciente para editar

class edit_pacientes_form(forms.Form):

    # Campos del formulario
    id = forms.CharField(label = 'id Paciente:', max_length = 10, required = False)
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
