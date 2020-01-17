from django import forms
from django.forms import ModelForm, Textarea, TextInput, NumberInput, Select, EmailInput, HiddenInput, CheckboxInput
from fixuSystem.progvars import selTipoEquip, selCtrlEquip
from .models import Clinica, Consultorio, Equipamiento, Proveedor, Profesional
from django.conf import settings



#################################
#                               #
#       FORMS DE CLINICA        #
#                               #
#################################

class init_edit_info_clinica_form(ModelForm):

    class Meta:
        model = Clinica
        exclude = ['firstupdated', 'lastupdated', 'modifiedby']
        widgets = {            
            'clinicname': TextInput(attrs={'style': 'width: 300px'}), 
            'nif': TextInput(attrs={'style': 'width: 200px'}), 
            'ownerfullname': TextInput(attrs={'style': 'width: 300px'}), 
            'dni': TextInput(attrs={'style': 'width: 200px'}),
            'numcolegiado': TextInput(attrs={'style': 'width: 200px'}),
            'fulladdress': TextInput(attrs={'style': 'width: 300px'}),
            'city': TextInput(attrs={'style': 'width: 200px'}),
            'postcode': NumberInput(attrs={'style': 'width: 200px', 'min': 0, 'max': 99999}),
            'province': TextInput(attrs={'style': 'width: 200px'}),
            'phone1': NumberInput(attrs={'style': 'width: 200px', 'min': 0, 'max': 999999999}),
            'phone2': NumberInput(attrs={'style': 'width: 200px', 'min': 0, 'max': 999999999}),
            'email': EmailInput(attrs={'style': 'width: 200px'}),
            'notes': Textarea(attrs={'cols': 70, 'rows': 3})
            }



#################################
#                               #
#     FORMS DE CONSULTORIOS     #
#                               #
#################################

class create_edit_consultorios_form(ModelForm):

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

# Form de filtro para consultorio
class customConsultorioForm(forms.Form):

    filterdesc = forms.CharField(label = 'DESCR', required = False, max_length = 10)
    filterdesc.widget = forms.widgets.TextInput(attrs={'style': 'width: 100px'})
    filterlocat = forms.CharField(label = 'LOCAL', required = False, max_length = 10)
    filterlocat.widget = forms.widgets.TextInput(attrs={'style': 'width: 100px'})



#################################
#                               #
#     FORMS DE EQUIPAMIENTO     #
#                               #
#################################

class create_edit_equipamiento_form(ModelForm):

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
            'notes': Textarea(attrs={'cols': 56, 'rows': 3})
        }

# Widget de filtrado de tipo de equipamiento
class customEquipamientoWidget(forms.widgets.Select):

    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        list_choices = list()
        list_choices.append(('---', '---'))
        list_choices.extend(selTipoEquip)
        self.choices = list_choices

# Widget de filtrado de control de equipamiento
class customCtrlEquipamientoWidget(forms.widgets.Select):

    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        list_choices = list()
        list_choices.append(('---', '---'))
        list_choices.extend(selCtrlEquip)
        self.choices = list_choices

# Form de filtro para control de equipamiento
class customEquipamientoForm(forms.Form):

    filtertype = forms.CharField(label = 'Tipo', widget = customEquipamientoWidget())
    filterdesc = forms.CharField(label = 'Descripción', required = False, max_length = 10)
    filterdesc.widget = forms.widgets.TextInput(attrs={'style': 'width: 80px'})
    filterctrl = forms.CharField(label = 'Ctrl', widget = customCtrlEquipamientoWidget())



#################################
#                               #
#      FORMS DE PROVEEDORES     #
#                               #
#################################

class create_edit_proveedores_form(ModelForm):

    class Meta:
        model = Proveedor
        exclude = ['firstupdated', 'lastupdated', 'modifiedby']
        widgets = {
            'fullname': TextInput(attrs={'style': 'width: 320px'}),
            'area': TextInput(attrs={'style': 'width: 180px'}),
            'owner': TextInput(attrs={'style': 'width: 320px'}),
            'nif': TextInput(attrs={'style': 'width: 180px'}),
            'fulladdress': TextInput(attrs={'style': 'width: 630px'}),
            'contactManufact': TextInput(attrs={'style': 'width: 630px'}),
            'phoneManufact': NumberInput(attrs={'style': 'width: 120px', 'min': 0, 'max': 999999999}),
            'emailManufact': EmailInput(attrs={'style': 'width: 180px'}),
            'contactProveedor': TextInput(attrs={'style': 'width: 630px'}),
            'phoneProveedor': NumberInput(attrs={'style': 'width: 120px', 'min': 0, 'max': 999999999}),
            'emailProveedor': EmailInput(attrs={'style': 'width: 180px'}),
            'contactSAT': TextInput(attrs={'style': 'width: 630px'}),
            'phoneSAT': NumberInput(attrs={'style': 'width: 120px', 'min': 0, 'max': 999999999}),
            'emailSAT': EmailInput(attrs={'style': 'width: 180px'}),
            'notas': Textarea(attrs={'cols': 76, 'rows': 2})
        }

# Form de filtro para proveedor
class customProveedorForm(forms.Form):

    filtername = forms.CharField(label = 'Empresa', required = False, max_length = 10)
    filtername.widget = forms.widgets.TextInput(attrs={'style': 'width: 100px'})
    filterarea = forms.CharField(label = 'Area', required = False, max_length = 10)
    filterarea.widget = forms.widgets.TextInput(attrs={'style': 'width: 100px'})



#################################
#                               #
#     FORMS DE PROFESIONALES    #
#                               #
#################################

class create_edit_profesionales_form(ModelForm):

    user_login = forms.CharField(label = 'Usuario/a', max_length = 150, required = True)
    user_login.widget = forms.widgets.TextInput(attrs={'style':'width: 300px'})
    user_password = forms.CharField(label = 'Clave', max_length = 150, required = True)
    user_password.widget = forms.widgets.PasswordInput(attrs={'style':'width: 300px'})
    user_isactive = forms.BooleanField(label='Activo/a', required = False, initial = True)    
    user_issuperuser = forms.BooleanField(label='Superusuario/a', required = False)    
    user_isstaff = forms.BooleanField(label='Administrador/a', required = False)

    class Meta:
        model = Profesional
        exclude = ['oto_Profesional', 'firstupdated', 'lastupdated', 'modifiedby']
        widgets = {
            'fullname': TextInput(attrs={'style':'width: 175px'}),
            'dni': TextInput(attrs={'style': 'width: 175px'}),
            'numcolegiado': TextInput(attrs={'style': 'width: 175px'}),
            'nif': TextInput(attrs={'style': 'width: 175px'}),
            'position': TextInput(attrs={'style': 'width: 175px'}),
            'department': TextInput(attrs={'style': 'width: 175px'}),
            'fulladdress': TextInput(attrs={'style': 'width: 510px'}),
            'postcode': NumberInput(attrs={'style': 'width: 175px', 'min': 0, 'max': 99999}),
            'city': TextInput(attrs={'style': 'width: 175px'}),
            'province': TextInput(attrs={'style': 'width: 175px'}),
            'country': TextInput(attrs={'style': 'width: 175px'}),
            'phone1': NumberInput(attrs={'style': 'width: 120px', 'min': 0, 'max': 999999999}),
            'phone2': NumberInput(attrs={'style': 'width: 120px', 'min': 0, 'max': 999999999}),
            'email': EmailInput(attrs={'style': 'width: 175px'}),
            'notes': Textarea(attrs={'cols': 62, 'rows': 3})
        }

# Selección de profesionales
class select_profesionales_form(forms.Form):

    fullname = forms.CharField(label = 'Nombre', max_length = 10, required = False)
    position = forms.CharField(label = 'Cargo', max_length = 10, required = False)
    department = forms.CharField(label = 'Departamento',  max_length = 10, required = False)
