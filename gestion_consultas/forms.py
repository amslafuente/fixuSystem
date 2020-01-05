from django import forms
from django.forms import ModelForm
from gestion_citas.models import Cita
from .models import Consulta
from django.forms import ModelForm, Textarea, DateInput, TimeInput, Select
from fixuSystem.progvars import selOrder

class select_paciente_consultas_form(forms.Form):

    # Campos del formulario
    dni = forms.CharField(label = 'DNI:', max_length = 10, required = False)
    name = forms.CharField(label = 'Nombre:', max_length = 10, required = False)
    familyname = forms.CharField(label = 'Apellidos:',  max_length = 10, required = False)
    orderby = forms.ChoiceField(label = 'Ordenar por:', choices = selOrder)
    orderby.widget = Select(attrs={'style': 'width: 242px;'}, choices = selOrder)
