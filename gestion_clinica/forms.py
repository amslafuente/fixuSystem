########## Forms de gestion_clinica ##########

from django import forms
from django.forms import ModelForm, Textarea, TextInput, NumberInput
from .models import Clinica, Consultorio
from django.conf import settings

###############################################################################

# Form para crear clinica

class init_edit_info_clinica_form(forms.ModelForm):

    class Meta:
        model = Clinica
        exclude = ['firstupdated', 'lastupdated', 'modifiedby']
        widgets = {
            'notes': Textarea(attrs={'cols': 80, 'rows': 5})
            }

###############################################################################

# Form para crear consultorios

class create_edit_consultorios_form(forms.ModelForm):

    class Meta:
        model = Consultorio
        exclude = ['firstupdated', 'lastupdated', 'modifiedby']
        widgets = {
            'officeID': TextInput(attrs={'style': 'width: 430px'}),
            'officeDesc': TextInput(attrs={'style': 'width: 430px'}),
            'officeLocation': TextInput(attrs={'style': 'width: 430px'}),
            'officeDepartment': TextInput(attrs={'style': 'width: 430px'}),
            'officePhone': NumberInput(attrs={'style': 'width: 150px', 'min': 0, 'max': 999999999}),
            'officeEquipment': Textarea(attrs={'cols': 40, 'rows': 3}),
            'officeNotes': Textarea(attrs={'cols': 40, 'rows': 3})
            }

###############################################################################
