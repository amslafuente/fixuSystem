########## Forms de gestion_clinica ##########

from django import forms
from django.forms import ModelForm, Textarea, TextInput, NumberInput, Select, EmailInput, HiddenInput
#from django.forms import forms, fields, widgets
from fixuSystem.progvars import selTipoEquip
from .models import Clinica, Consultorio, Equipamiento, Proveedor, Profesional
from django.conf import settings

# Form para crear clinica
class init_edit_info_clinica_form(ModelForm):

    class Meta:
        model = Clinica
        exclude = ['firstupdated', 'lastupdated', 'modifiedby']
        widgets = {
            'notes': Textarea(attrs={'cols': 80, 'rows': 5})
            }

# Form para crear consultorios
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

    filterdesc = forms.CharField(label = 'Descrip.', required = False, max_length = 10)
    filterdesc.widget = forms.widgets.TextInput(attrs={'style': 'width: 100px'})
    filterlocat = forms.CharField(label = 'Situac.', required = False, max_length = 10)
    filterlocat.widget = forms.widgets.TextInput(attrs={'style': 'width: 100px'})

# Form para crear equipamiento
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
            'notes': Textarea(attrs={'cols': 57, 'rows': 2})
            }

# Widget de filtrado de tipo de equipamiento
class customEquipamientoWidget(forms.widgets.Select):

    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        list_choices = list()
        list_choices.append(('todos', 'Todos'))
        list_choices.extend(selTipoEquip)
        self.choices = list_choices

# Form de filtro para equipamiento
class customEquipamientoForm(forms.Form):

    filter_ = forms.CharField(label = 'Filtro', widget = customEquipamientoWidget())
    condition = forms.CharField(label = 'Condición', required = False, max_length = 10)
    condition.widget = forms.widgets.TextInput(attrs={'style': 'width: 80px'})
    ctrl = forms.CharField(label = 'Ctrl', required = False, max_length = 10)
    ctrl.widget = forms.widgets.Select(attrs={'style': 'width: 80px'}, choices=[('', ''), ('oper', 'Oper'), ('stock', 'Stock')])

# Form para crear proveedores
class create_edit_proveedores_form(ModelForm):

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

# Form de filtro para proveedor
class customProveedorForm(forms.Form):

    filtername = forms.CharField(label = 'Empresa', required = False, max_length = 10)
    filtername.widget = forms.widgets.TextInput(attrs={'style': 'width: 100px'})
    filterarea = forms.CharField(label = 'Area', required = False, max_length = 10)
    filterarea.widget = forms.widgets.TextInput(attrs={'style': 'width: 100px'})

# Form para seleccionar profesionales para mostrar
class select_profesionales_form(forms.Form):

    # Campos del formulario
    fullname = forms.CharField(label = 'Nombre:', max_length = 10, required = False)
    position = forms.CharField(label = 'Cargo:', max_length = 10, required = False)
    department = forms.CharField(label = 'Departamento:',  max_length = 10, required = False)

# Form para crear profesionales (mezcla User y Profesional)
class create_profesionales_form(ModelForm):

    user_login = forms.CharField(label = 'Usuario:', max_length = 150, required = True)
    user_login.widget = forms.widgets.TextInput(attrs={'style':'width: 200px'})
    user_password = forms.CharField(label = 'Password:', max_length = 150, required = True)
    user_password.widget = forms.widgets.PasswordInput(attrs={'style':'width: 200px'})
    user_issuperuser = forms.BooleanField(label='Es superusuario:', required = False)    
    user_isstaff = forms.BooleanField(label='Es staff:', required = False)


    class Meta:
        model = Profesional
        exclude = ['oto_Profesional', 'firstupdated', 'lastupdated', 'modifiedby']
        widgets = {
            'fullname': TextInput(attrs={'style':'width: 200px'}),
            'dni': TextInput(attrs={'style': 'width: 200px'}),
            'numcolegiado': TextInput(attrs={'style': 'width: 200px'}),
            'nif': TextInput(attrs={'style': 'width: 200px'}),
            'position': TextInput(attrs={'style': 'width: 200px'}),
            'department': TextInput(attrs={'style': 'width: 200px'}),
            'fulladdress': TextInput(attrs={'style': 'width: 544px'}),
            'postcode': NumberInput(attrs={'style': 'width: 200px', 'min': 0, 'max': 99999}),
            'city': TextInput(attrs={'style': 'width: 200px'}),
            'province': TextInput(attrs={'style': 'width: 200px'}),
            'country': TextInput(attrs={'style': 'width: 200px'}),
            'phone1': NumberInput(attrs={'style': 'width: 120px', 'min': 0, 'max': 999999999}),
            'phone2': NumberInput(attrs={'style': 'width: 120px', 'min': 0, 'max': 999999999}),
            'email': EmailInput(attrs={'style': 'width: 200px'}),
            'notes': Textarea(attrs={'cols': 60, 'rows': 3})
        }

# Form para editar profesionales (mezcla User y Profesional)
class edit_profesionales_form(ModelForm):

    user_login = forms.CharField(label = 'Usuario:', max_length = 150, required = True)
    user_login.widget = forms.widgets.TextInput(attrs={'style':'width: 200px'})
    user_password = forms.CharField(label = 'Password:', max_length = 150, required = True)
    user_password.widget = forms.widgets.HiddenInput()
    user_isactive = forms.BooleanField(label='Activo:', required = False)    
    user_issuperuser = forms.BooleanField(label='Es superusuario:', required = False)    
    user_isstaff = forms.BooleanField(label='Es staff:', required = False)

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
            'fulladdress': TextInput(attrs={'style': 'width: 514px'}),
            'postcode': NumberInput(attrs={'style': 'width: 175px', 'min': 0, 'max': 99999}),
            'city': TextInput(attrs={'style': 'width: 175px'}),
            'province': TextInput(attrs={'style': 'width: 175px'}),
            'country': TextInput(attrs={'style': 'width: 175px'}),
            'phone1': NumberInput(attrs={'style': 'width: 120px', 'min': 0, 'max': 999999999}),
            'phone2': NumberInput(attrs={'style': 'width: 120px', 'min': 0, 'max': 999999999}),
            'email': EmailInput(attrs={'style': 'width: 175px'}),
            'notes': Textarea(attrs={'cols': 60, 'rows': 3})
        }

# Form para completar profesionales (mezcla User y Profesional)
class complete_profesionales_form(ModelForm):

    class Meta:
        model = Profesional
        exclude = ['firstupdated', 'lastupdated', 'modifiedby']
        widgets = {
            'oto_Profesional': HiddenInput(),
            'fullname': TextInput(attrs={'style':'width: 175px'}),
            'dni': TextInput(attrs={'style': 'width: 175px'}),
            'numcolegiado': TextInput(attrs={'style': 'width: 175px'}),
            'nif': TextInput(attrs={'style': 'width: 175px'}),
            'position': TextInput(attrs={'style': 'width: 175px'}),
            'department': TextInput(attrs={'style': 'width: 175px'}),
            'fulladdress': TextInput(attrs={'style': 'width: 514px'}),
            'postcode': NumberInput(attrs={'style': 'width: 175px', 'min': 0, 'max': 99999}),
            'city': TextInput(attrs={'style': 'width: 175px'}),
            'province': TextInput(attrs={'style': 'width: 175px'}),
            'country': TextInput(attrs={'style': 'width: 175px'}),
            'phone1': NumberInput(attrs={'style': 'width: 120px', 'min': 0, 'max': 999999999}),
            'phone2': NumberInput(attrs={'style': 'width: 120px', 'min': 0, 'max': 999999999}),
            'email': EmailInput(attrs={'style': 'width: 175px'}),
            'notes': Textarea(attrs={'cols': 60, 'rows': 3})
        }
