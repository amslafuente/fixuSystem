########## Forms de gestion_clinica ##########

from django import forms
from django.forms import ModelForm, Textarea, TextInput, NumberInput, Select, EmailInput
from .models import Clinica, Consultorio, Equipamiento, Proveedor
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

# Form para crear equipamiento

class create_edit_equipamiento_form(forms.ModelForm):

    class Meta:
        model = Equipamiento
        exclude = ['firstupdated', 'lastupdated', 'modifiedby']
        widgets = {
            'equipID': TextInput(attrs={'style': 'width: 360px'}),
            'equipDesc': TextInput(attrs={'style': 'width: 360px'}),
            'equipType': Select(attrs={'style': 'width: 360px'}),
            'fk_Location': Select(attrs={'style': 'width: 360px'}),
            'equipDepartment': TextInput(attrs={'style': 'width: 360px'}),
            'fk_Manufact': Select(attrs={'style': 'width: 360px'}),
            'fk_Proveedor': Select(attrs={'style': 'width: 360px'}),
            'fk_SAT': Select(attrs={'style': 'width: 360px'}),
            'stocklimit': NumberInput(attrs={'style': 'width: 85px', 'min': 0, 'max': 99999}),
            'stockavail': NumberInput(attrs={'style': 'width: 85px', 'min': 0, 'max': 99999}),
            'notes': Textarea(attrs={'cols': 57, 'rows': 2})
            }

###############################################################################

# Form para crear proveedores

class create_edit_proveedores_form(forms.ModelForm):

    class Meta:
        model = Proveedor
        exclude = ['firstupdated', 'lastupdated', 'modifiedby']
        widgets = {
            'fullname': TextInput(attrs={'style': 'width: 320px'}),
            'area': TextInput(attrs={'style': 'width: 224px'}),
            'owner': TextInput(attrs={'style': 'width: 320px'}),
            'nif': TextInput(attrs={'style': 'width: 224px'}),
            'fulladdress': TextInput(attrs={'style': 'width: 710px'}),
            'contactManufact': TextInput(attrs={'style': 'width: 686px'}),
            'phoneManufact': NumberInput(attrs={'style': 'width: 120px', 'min': 0, 'max': 999999999}),
            'emailManufact': EmailInput(attrs={'style': 'width: 300px'}),
            'contactProveedor': TextInput(attrs={'style': 'width: 686px'}),
            'phoneProveedor': NumberInput(attrs={'style': 'width: 122px', 'min': 0, 'max': 999999999}),
            'emailProveedor': EmailInput(attrs={'style': 'width: 302px'}),
            'contactSAT': TextInput(attrs={'style': 'width: 686px'}),
            'phoneSAT': NumberInput(attrs={'style': 'width: 135px', 'min': 0, 'max': 999999999}),
            'emailSAT': EmailInput(attrs={'style': 'width: 315px'}),
            'notas': Textarea(attrs={'cols': 82, 'rows': 2})
            }
