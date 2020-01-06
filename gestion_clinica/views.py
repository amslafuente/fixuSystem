########## Views de gestion_clinica ###########

from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.http import request, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, TemplateView, DeleteView
from django.views import View
from django.contrib import messages
from .models import Clinica, Profesional, Consultorio, Equipamiento, Proveedor
from django.contrib.auth.models import User
from .forms import init_edit_info_clinica_form, create_edit_consultorios_form, create_edit_equipamiento_form
from .forms import customConsultorioForm, customEquipamientoForm, customProveedorForm
from .forms import select_profesionales_form, create_edit_profesionales_form
from .forms import create_edit_proveedores_form
import os
from pathlib import Path
from django.conf import settings
from django.forms import forms, fields, widgets
from fixuSystem.progvars import selTipoEquip

########## MUESTRA MENU DE GESTION DE SERVICIOS ##########

@method_decorator(login_required, name='dispatch')
class instalac_servic_clinica_view(TemplateView):
    template_name = 'instalac_servic_clinica_tpl.html'

##################################################
#                     CLINICA                    #
##################################################

########## MUESTRA DATOS DE CLINICA ##########

class info_clinica_view(View):

    def get(self, request):

        # Recupera el primer registro encontrado, que es el que vale
        qs = Clinica.objects.first()
        ctx = dict()
        ctx['clinica'] = qs

        return render (request, 'info_clinica_tpl.html', ctx)

 ########## INICIALIZA DATOS DE CLINICA ##########

@method_decorator(login_required, name='dispatch')
class init_clinica_view(View):

    # POST al volver del formulario
    def post(self, request):

        # Se meten los datos del formulario
        ctx= dict()
        form = init_edit_info_clinica_form(request.POST, request.FILES)

        # Si el formulario es valido
        if form.is_valid():
            # Almacena temporalmente
            clinica = form.save(commit = False)
            # Datos de control
            if str(self.request.user) != 'AmonymousUser':
                clinica.modifiedby = str(self.request.user)
            else:
                clinica.modifiedby = 'unix:' + str(self.request.META['USERNAME'])
            # Finalmente guarda
            clinica.save()

            # Si se ha subido una foto, a los datos de la clinica le cambia
            # el nombre a 'logo-clinica", (SIN EXTENSION; PARA QUE VALGA CUALQUIER FORMATO RECONOCIDO)
            # respetando la ruta "clinica/<nombre>"
            # Quedaría "clinica/<logo-clinica"
            try:
                # Recupera la clinica
                inter_clinica = Clinica.objects.first()

                # Si se introduce un nombre de archivo
                split_name = str(inter_clinica.picturefile)
                if split_name != '':
                    # Trocea el nombre de la ruta por "/" y "."
                    # La parte del nombre es todo minusculas
                    new_name = split_name.split('/')[0] + '/logo-clinica'
                    # Si ya existe un archivo con ese nombre lo borra antes de subir el nuevo
                    if Path(new_name).is_file():
                        os.remove(new_name)
                    # Sustituye al picture file original por el nuevo
                    inter_clinica.picturefile = new_name
                    # Limpia y guarda el registro
                    inter_clinica.save()
                    # Cambia el nombre del archivo en el disco
                    os.rename(str(settings.MEDIA_ROOT + '/' + split_name), str(settings.MEDIA_ROOT +'/' + new_name))
            except:
                messages.warning(request, 'Error procesando archivo de imagen')

            return HttpResponseRedirect(reverse('info-clinica'))

        # Si la form no es valida recarga co  los errores
        else:
            # Mensajes de error
            messages.warning(request, 'Errores en el formulario')
            # Regresa al formulario
            ctx['form'] = form
            
            return render(request, 'init_info_clinica_tpl.html', ctx)

    # GET al llamar a la view
    def get(self, request):

        # Si el usuario no es superuser no permite acceder a los datos de la clinica
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))
        
        # Cuenta los registros de la base de datos Clinica
        qs_count = Clinica.objects.count()

        # Si ya existe un registro avisa de que solo se puede editar, no crear
        if qs_count > 0:
            return HttpResponseRedirect(reverse('error-init-clinica'))
        # Si no existe pasa a crearlo
        else:
            ctx = dict()
            # Asocia la form y la pasa al contexto
            form = init_edit_info_clinica_form()
            ctx['form'] = form

            return render(request, 'init_info_clinica_tpl.html', ctx)

# Error si el usuario NO ES SUPERUSUARIO
@method_decorator(login_required, name='dispatch')
class error_privilegios_clinica_view(TemplateView):
    template_name = 'error_privilegios_clinica_tpl.html'

# Error si ya existe un registro y se pretende crear otro
@method_decorator(login_required, name='dispatch')
class error_init_clinica_view(TemplateView):
    template_name = 'error_init_clinica_tpl.html'

########## EDITA DATOS DE CLINICA ##########

@method_decorator(login_required, name='dispatch')
class edit_info_clinica_view(UpdateView):

    model = Clinica
    context_object_name ='clinica'
    pk_url_kwarg = 'idClinica'
    form_class = init_edit_info_clinica_form
    template_name = 'edit_info_clinica_tpl.html'

    # Con el GET comprueba si el usuario tiene privilegios
    def get(self, request, *args, **kwargs):

        # Si no es superusuario no permite acceder a los datos de clinica
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))
        else:
            return super().get(request, *args, **kwargs)

    # Actualiza el campo modifiedby y la foto
    def form_valid(self, form):

        # Pone los registros de control que faltan en una instancia "manejable": clinica
        # Commit = False: evita que se guarde ya en la base de datos
        clinica = form.save(commit = False)
        # Campos de control
        if str(self.request.user) != 'AmonymousUser':
            clinica.modifiedby = str(self.request.user)
        else:
            clinica.modifiedby = 'unix:' + str(self.request.META['USERNAME'])
        # Limpia y guarda el registro
        clinica.save()

        # Si se actualiza el logo se renombra a 'logo-clinica' (sin extension) y se borra el antiguo
        if 'picturefile' in form.changed_data:
            picture_changed = True
        else:
            picture_changed = False
      
        if picture_changed:
            try:
                # Recupera la clinica
                inter_clinica = Clinica.objects.first()
                # Si se introduce un nombre de archivo
                split_name = str(inter_clinica.picturefile)
                if split_name != '':
                    # Trocea el nombre de la ruta por "/" y "."
                    # La parte del DNI es todo mayusculas
                    new_name = split_name.split('/')[0] + '/logo-clinica'
                    # Si ya existe un archivo con ese nombre lo borra antes de subir el nuevo
                    if Path(new_name).is_file():
                        os.remove(new_name)
                    # Sustituye al picture file original por el nuevo
                    inter_clinica.picturefile = new_name
                    # Limpia y guarda el registro
                    inter_clinica.save()
                    # Cambia el nombre del archivo en el disco
                    os.rename(str(settings.MEDIA_ROOT + '/' + split_name), str(settings.MEDIA_ROOT +'/' + new_name))
            except:
                messages.warning(request, 'Error procesando archivo de imagen')

        return HttpResponseRedirect(reverse('info-clinica'))

##################################################
#                 CONSULTORIOS                   #
##################################################

##### MUESTRA EL ID CONSULTORIO CONCRETO #####

@method_decorator(login_required, name='dispatch')
class id_consultorios_view(DetailView):

    model = Consultorio
    context_object_name = 'consultorios'
    pk_url_kwarg = 'idConsultorio'
    template_name = 'id_consultorios_tpl.html'

    def get_queryset(self):

        # Extrae el consultorio en cuestion
        qs = Consultorio.objects.filter(idConsultorio__exact = self.kwargs['idConsultorio'])
        
        return qs

##### LISTADO DE CONSULTORIOS #####

@method_decorator(login_required, name='dispatch')
class listado_consultorios_view(ListView):

    model = Consultorio
    context_object_name = 'consultorios'
    paginate_by = 20
    template_name = 'listado_consultorios_tpl.html'

    def get_queryset(self):
    
        qs = super().get_queryset()
        # Extrae registros del GET o los pone por defecto
        kwarg_filterdesc = (self.request.GET.get('filterdesc') or '').lower()
        kwarg_filterlocat = (self.request.GET.get('filterlocat') or '').lower()
        kwarg_orderby = (self.request.GET.get('orderby') or '')

       # Fullname
        if kwarg_filterdesc == '':
            qs = Consultorio.objects.all().order_by('officeID')
        else:
            qs = Consultorio.objects.filter(officeID__icontains = kwarg_filterdesc).order_by('officeID')

        # Area
        if kwarg_filterlocat != '':
            qs = qs.filter(officeLocation__icontains = kwarg_filterlocat)
        
        # OrderBy ASC
        if kwarg_orderby != '':
            qs = qs.order_by(kwarg_orderby)

        return qs

    def get_context_data(self, **kwargs):
    
        ctx = super().get_context_data(**kwargs)
        # Form al contexto
        filterform = customConsultorioForm(self.request.GET) or customConsultorioForm()
        ctx['form'] = filterform
        # Obtiene el filtro y condicion actual del GET   
        ctx['filterdesc'] = (self.request.GET.get('filterdesc') or '').lower()
        ctx['filterlocat'] = (self.request.GET.get('filterlocat') or '').lower()
        ctx['orderby'] = (self.request.GET.get('orderby') or '')

        return ctx

########## EDITA DATOS DE CLINICA ##########

@method_decorator(login_required, name='dispatch')
class create_consultorios_view(CreateView):

    model = Consultorio
    context_object_name = 'consultorios'
    pk_url_kwarg = 'idConsultorio'
    form_class = create_edit_consultorios_form
    template_name = 'create_consultorios_tpl.html'

    # Formulario correcto
    def form_valid(self, form):

        consultorio = form.save(commit = False)
        # Campos de control
        if str(self.request.user) != 'AmonymousUser':
            consultorio.modifiedby = str(self.request.user)
        else:
            consultorio.modifiedby = 'unix:' + str(self.request.META['USERNAME'])
        # Limpia y guarda el registro
        consultorio.save()

        return HttpResponseRedirect(reverse('listado-consultorios'))

    # GET al llamar a la view
    def get(self, request):

        # Si el usuario no es o staff no permite acceder a los datos de la clinica
        if (not request.user.is_superuser) and (not request.user.is_staff):
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))

        return super().get(request)

@method_decorator(login_required, name='dispatch')
class edit_consultorios_view(UpdateView):

    model = Consultorio
    context_object_name = 'consultorios'
    pk_url_kwarg = 'idConsultorio'
    form_class = create_edit_consultorios_form
    template_name = 'edit_consultorios_tpl.html'

    # GET al llamar a la view
    def get(self, request, **kwargs):

        # Si el usuario no es o staff no permite acceder a los datos de la clinica
        if (not request.user.is_superuser) or (not request.user.is_staff):
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))

        return super().get(request)

@method_decorator(login_required, name='dispatch')
class delete_consultorios_view(DeleteView):

    model = Consultorio
    context_object_name = 'consultorios'
    pk_url_kwarg = 'idConsultorio'
    form_class = create_edit_consultorios_form
    template_name = 'delete_consultorios_tpl.html'
    success_url = reverse_lazy('listado-consultorios')

    def get_queryset(self):

        # Extrae el consultorio en cuestion
        qs = Consultorio.objects.filter(idConsultorio__exact = self.kwargs['idConsultorio'])

        return qs

    # GET al llamar a la view
    def get(self, request, **kwargs):

        # Si el usuario no es o staff no permite acceder a los datos de la clinica
        if (not request.user.is_superuser) or (not request.user.is_staff):
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))

        return super().get(request)

##################################################
#                   EQUIPAMIENTO                 #
##################################################

##### ID DE EQUIPAMIENTO #####

@method_decorator(login_required, name='dispatch')
class id_equipamiento_view(DetailView):

    model = Equipamiento
    context_object_name = 'equipamientos'
    pk_url_kwarg = 'idEquipamiento'
    template_name = 'id_equipamiento_tpl.html'

    def get_queryset(self, **kwargs):

        # Extrae el equipo en cuestion
        qs = Equipamiento.objects.filter(idEquipamiento__exact = self.kwargs['idEquipamiento'])
        
        return qs

##### LISTADO DE EQUIPAMIENTO #####

@method_decorator(login_required, name='dispatch')
class listado_equipamiento_view(ListView):
    
    model = Equipamiento
    context_object_name = 'equipamientos'
    paginate_by = 20
    template_name = 'listado_equipamiento_tpl.html'
 
    def get_queryset(self):

        qs = super().get_queryset()
        # Extrae registros del GET o los pone por defecto
        kwarg_filter = (self.request.GET.get('filter_') or 'todos').lower()
        kwarg_condition = (self.request.GET.get('condition') or '').lower()
        kwarg_ctrl = (self.request.GET.get('ctrl') or '').lower()
        kwarg_orderby = (self.request.GET.get('orderby') or '')

       # Filter_
        if kwarg_filter == 'todos':
            qs = Equipamiento.objects.all().order_by('equipDesc')
        else:
            qs = Equipamiento.objects.filter(equipType__icontains = kwarg_filter).order_by('equipDesc')

        # Condit
        if kwarg_condition != '':
            qs = qs.filter(equipDesc__icontains = kwarg_condition)
        
        # Ctrl
        if kwarg_ctrl == 'stock':
            qs = qs.filter(stockwarning = True)
        elif kwarg_ctrl == 'oper':
            qs = qs.filter(stockwarning = False)

        # OrderBy ASC
        if kwarg_orderby != '':
            qs = qs.order_by(kwarg_orderby)

        return qs

    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)
        # Form al contexto
        filterform = customEquipamientoForm(self.request.GET) or customEquipamientoForm()
        ctx['form'] = filterform
        # Obtiene el filtro y condicion actual del GET   
        ctx['filter'] = (self.request.GET.get('filter_') or 'todos').lower()
        ctx['condition'] = (self.request.GET.get('condition') or '').lower()
        ctx['ctrl'] = (self.request.GET.get('ctrl') or '').lower()
        ctx['orderby'] = (self.request.GET.get('orderby') or '')

        return ctx

##### CREACION Y EDICION DE EQUIPAMIENTO #####

@method_decorator(login_required, name='dispatch')
class create_equipamiento_view(CreateView):

    model = Equipamiento
    context_object_name = 'equipamientos'
    pk_url_kwarg = 'idEquipamiento'
    form_class = create_edit_equipamiento_form
    template_name = 'create_equipamiento_tpl.html'
    
    # Formulario correcto
    def form_valid(self, form):

        equipamiento = form.save(commit = False)
        # Calcula el stockratio
        if form.cleaned_data['stocklimit'] > 0:
            equipamiento.stockratio = (form.cleaned_data['stockavail'] * 100 // form.cleaned_data['stocklimit'])
        else:
            equipamiento.stockratio = 0
        if equipamiento.stockratio > 100:
            equipamiento.stockratio = 100
        # Campos de control
        if str(self.request.user) != 'AmonymousUser':
            equipamiento.modifiedby = str(self.request.user)
        else:
            equipamiento.modifiedby = 'unix:' + str(self.request.META['USERNAME'])
        # Limpia y guarda el registro
        equipamiento.save()

        return HttpResponseRedirect(reverse('listado-equipamiento'))

    def form_invalid(self, form):

        messages.warning(self.request, 'Errores en el formulario.')
        
        return super().form_invalid(form)

    # GET al llamar a la view
    def get(self, request):

        # Si el usuario no es o staff no permite acceder a los datos de la clinica
        if (not request.user.is_superuser) and (not request.user.is_staff):
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))

        return super().get(request)

@method_decorator(login_required, name='dispatch')
class edit_equipamiento_view(UpdateView): 

    model = Equipamiento
    context_object_name = 'equipamiento'
    pk_url_kwarg = 'idEquipamiento'
    form_class = create_edit_equipamiento_form
    template_name = 'edit_equipamiento_tpl.html'

    # Formulario correcto
    def form_valid(self, form):

        equipamiento = form.save(commit = False)
        # Calcula el stockratio
        if form.cleaned_data['stocklimit'] > 0:
            equipamiento.stockratio = (form.cleaned_data['stockavail'] * 100 // form.cleaned_data['stocklimit'])
        else:
            equipamiento.stockratio = 0
        if equipamiento.stockratio > 100:
            equipamiento.stockratio = 100
        # Campos de control
        if str(self.request.user) != 'AmonymousUser':
            equipamiento.modifiedby = str(self.request.user)
        else:
            equipamiento.modifiedby = 'unix:' + str(self.request.META['USERNAME'])
        # Limpia y guarda el registro
        equipamiento.save()

        return HttpResponseRedirect(reverse('id-equipamiento', args=[equipamiento.idEquipamiento]))

    # GET al llamar a la view
    def get(self, request, **kwargs):

        # Si el usuario no es o staff no permite acceder a los datos de la clinica
        if (not request.user.is_superuser) or (not request.user.is_staff):
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))

        return super().get(request)

@method_decorator(login_required, name='dispatch')
class delete_equipamiento_view(DeleteView):

    model = Equipamiento
    context_object_name = 'equipamientos'
    pk_url_kwarg = 'idEquipamiento'
    template_name = 'delete_equipamiento_tpl.html'
    success_url = reverse_lazy('listado-equipamiento')

    def get_queryset(self):

        # Extrae el consultorio en cuestion
        qs = Equipamiento.objects.filter(idEquipamiento__exact = self.kwargs['idEquipamiento'])

        return qs

    # GET al llamar a la view
    def get(self, request, **kwargs):

        # Si el usuario no es o staff no permite acceder a los datos de la clinica
        if (not request.user.is_superuser) or (not request.user.is_staff):
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))

        return super().get(request)

##################################################
#                   PROVEEDORES                  #
##################################################

##### ID DE PROVEEDORES #####

@method_decorator(login_required, name='dispatch')
class id_proveedores_view(DetailView):

    model = Proveedor
    context_object_name = 'proveedores'
    pk_url_kwarg = 'idProveedor'
    template_name = 'id_proveedores_tpl.html'

    def get_queryset(self, **kwargs):

        # Extrae el equipo en cuestion
        qs = Proveedor.objects.filter(idProveedor__exact = self.kwargs['idProveedor'])
        
        return qs

##### LISTADO DE PROVEEDORES #####

@method_decorator(login_required, name='dispatch')
class listado_proveedores_view(ListView):
    
    model = Proveedor
    context_object_name = 'proveedores'
    paginate_by = 20
    template_name = 'listado_proveedores_tpl.html'
 
    def get_queryset(self):

        qs = super().get_queryset()
        # Extrae registros del GET o los pone por defecto
        kwarg_filtername = (self.request.GET.get('filtername') or '').lower()
        kwarg_filterarea = (self.request.GET.get('filterarea') or '').lower()
        kwarg_orderby = (self.request.GET.get('orderby') or '')

       # Fullname
        if kwarg_filtername == '':
            qs = Proveedor.objects.all().order_by('fullname')
        else:
            qs = Proveedor.objects.filter(fullname__icontains = kwarg_filtername).order_by('fullname')

        # Area
        if kwarg_filterarea != '':
            qs = qs.filter(area__icontains = kwarg_filterarea)
        
         # OrderBy
        if kwarg_orderby != '':
            qs = qs.order_by(kwarg_orderby)

        return qs

    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)
        # Pasa el form y el contexto
        filterform = customProveedorForm(self.request.GET) or customProveedorForm()
        ctx['form'] = filterform
        # Obtiene el filtro y condicion actual del GET   
        ctx['filtername'] = (self.request.GET.get('filtername') or '').lower()
        ctx['filterarea'] = (self.request.GET.get('filterarea') or '').lower()
        ctx['orderby'] = (self.request.GET.get('orderby') or '')

        return ctx

##### CREACION Y EDICION DE PROVEEDORES #####

@method_decorator(login_required, name='dispatch')
class create_proveedores_view(CreateView):

    model = Proveedor
    context_object_name = 'proveedores'
    pk_url_kwarg = 'idProveedor'
    form_class = create_edit_proveedores_form
    template_name = 'create_proveedores_tpl.html'
    
    # Formulario correcto
    def form_valid(self, form):

        proveedor = form.save(commit = False)
        # Campos de control
        if str(self.request.user) != 'AmonymousUser':
            proveedor.modifiedby = str(self.request.user)
        else:
            proveedor.modifiedby = 'unix:' + str(self.request.META['USERNAME'])
        # Limpia y guarda el registro
        proveedor.save()
        
        return HttpResponseRedirect(reverse('listado-proveedores'))

    def form_invalid(self, form):
        
        messages.warning(self.request, 'Errores en el formulario.')
        
        return super().form_invalid(form)

    # GET al llamar a la view
    def get(self, request):

        # Si el usuario no es o staff no permite acceder a los datos de la clinica
        if (not request.user.is_superuser) and (not request.user.is_staff):
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))

        return super().get(request)

@method_decorator(login_required, name='dispatch')
class edit_proveedores_view(UpdateView):

    model = Proveedor
    context_object_name = 'proveedores'
    pk_url_kwarg = 'idProveedor'
    form_class = create_edit_proveedores_form
    template_name = 'edit_proveedores_tpl.html'

    # Formulario correcto
    def form_valid(self, form):

        proveedor = form.save(commit = False)
        # Campos de control
        if str(self.request.user) != 'AmonymousUser':
            proveedor.modifiedby = str(self.request.user)
        else:
            proveedor.modifiedby = 'unix:' + str(self.request.META['USERNAME'])
        # Limpia y guarda el registro
        proveedor.save()

        return HttpResponseRedirect(reverse('id-proveedores', args=[proveedor.idProveedor]))

    # GET al llamar a la view
    def get(self, request, **kwargs):

        # Si el usuario no es o staff no permite acceder a los datos de la clinica
        if (not request.user.is_superuser) or (not request.user.is_staff):
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))

        return super().get(request)


@method_decorator(login_required, name='dispatch')
class delete_proveedores_view(DeleteView):

    model = Proveedor
    context_object_name = 'proveedores'
    pk_url_kwarg = 'idProveedor'
    template_name = 'delete_proveedores_tpl.html'
    success_url = reverse_lazy('listado-proveedores')

    def get_queryset(self):

        # Extrae el consultorio en cuestion
        qs = Proveedor.objects.filter(idProveedor__exact = self.kwargs['idProveedor'])

        return qs

    # GET al llamar a la view
    def get(self, request, **kwargs):

        # Si el usuario no es o staff no permite acceder a los datos de la clinica
        if (not request.user.is_superuser) or (not request.user.is_staff):
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))

        return super().get(request)

##################################################
#                   PROFESIONALES                #
##################################################

##### ID DE PROFESIONALES #####

@method_decorator(login_required, name='dispatch')
class profesionales_clinica_view(TemplateView):    
    template_name = 'profesionales_clinica_tpl.html'

##### SELECCIONA Y MUESTRA PROFESIONALES #####

@method_decorator(login_required, name='dispatch')
class select_profesionales_view(View):

    # POST
    def post(self, request):

        ctx = dict()
        # Rellena el form con el POST y añade al contexto
        form = select_profesionales_form(request.POST)

        # El form SI es validado
        if form.is_valid():
            # Devuelve las partes que interesan en una string para mostrar solo esos pacientes
            show_str = {'fullname':'fullname', 'position':'position', 'department':'department'}
            if str(form.cleaned_data['fullname']) != '':
                show_str['fullname'] = form.cleaned_data['fullname']
            if str(form.cleaned_data['position']) != '':
                show_str['position'] = form.cleaned_data['position']
            if str(form.cleaned_data['department']) != '':
                show_str['department'] = form.cleaned_data['department']

            return HttpResponseRedirect(reverse('listado-profesionales', kwargs = show_str))

        # El form NO es validado
        else:
            # Limpia el form y añade al contexto
            form = select_profesionales_form()
            ctx['form'] = form
            # Mensaje de error en contexto
            messages.warning(request, 'El formulario contiene errores')

            return render(request, 'select_profesionales_tpl.html', ctx)

    # GET
    def get(self, request):

        ctx = dict()
        # Limpia el form y lo añade al contexto
        form = select_profesionales_form()
        ctx['form'] = form
        
        return render(request, 'select_profesionales_tpl.html', ctx)


@method_decorator(login_required, name='dispatch')
class listado_profesionales_view(ListView):

    model = Profesional
    context_object_name = 'profesionales'
    template_name = 'listado_profesionales_tpl.html'
    paginate_by = 20

    # Modifica el query ALL para seleccionar los pacientes elegidos
    def get_queryset(self):

        # Filtrado del query por defecto
        qs = super().get_queryset()
        # Seleccion
        if self.kwargs['fullname'] != 'fullname':
            qs = qs.filter(fullname__icontains = self.kwargs['fullname'])
        if self.kwargs['position'] != 'position':
             qs = qs.filter(position__icontains = self.kwargs['position'])
        if self.kwargs['department'] != 'department':
             qs = qs.filter(department__icontains = self.kwargs['department'])
        # SELECT RELATED y ORDERBY de los campos y registros
        qs = qs.select_related('oto_Profesional').values('oto_Profesional', 'oto_Profesional__username', 'fullname', 'position', 'department', 'currentavail', 'currentstaff')
        qs = qs.order_by('fullname')
        
        return qs

@method_decorator(login_required, name='dispatch')
class id_profesionales_view(DetailView):

    model = Profesional
    context_object_name = 'profesionales'
    pk_url_kwarg = 'oto_Profesional'
    template_name = 'id_profesionales_tpl.html'

    def get_queryset(self):

        # Extrae el consultorio en cuestion
        qs = Profesional.objects.select_related('oto_Profesional').filter(oto_Profesional__exact = self.kwargs['oto_Profesional'])

        return qs

@method_decorator(login_required, name='dispatch')
class create_profesionales_view(View):

    # POST
    def post(self, request):

        # Si el usuario no es superuser no permite acceder a los datos
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))
  
        ctx = dict()
        
        # Pasa el fom al contexto
        form = create_edit_profesionales_form(request.POST, request.FILES)
        ctx['form'] = form

        # Primero crea el User de django, para luego pasarlo a oto_Profesional y validar el form
        djangouser = request.POST.get('djangouser', '')
        djangopassword = request.POST.get('djangopassword', '')
        django_issuper = request.POST.get('django_issuper', False)
        django_isstaff = request.POST.get('django_isstaff', False)
        
        if (djangouser != '' and djangopassword != ''):
            # Comprueba si existe ya ese usuario
            if User.objects.filter(username__exact = djangouser).exists():
                messages.warning(request, 'El usuario ya existe.')
                return render(request, 'create_profesionales_tpl.html', ctx)
            # Si no existe lo crea
            else:
                user = User.objects.create_user(djangouser, 'django@user.new', djangopassword)
                user.save()

        # Ahora valida el form
        if form.is_valid():

            # Pasa el form a un profesional
            profesional = form.save(commit = False)
            # Recupera el usuario creado
            user = User.objects.get(username__exact = djangouser)

            # Pone el oto_Profesional
            profesional.oto_Profesional = user
            # Pone los campos que faltan de user: email, is active, is staff, is superuser
            user.email = profesional.email
            user.is_active = True
            user.is_superuser = bool(django_issuper)
            if user.is_superuser:
                user.is_staff = True                
            else:    
                user.is_staff = bool(django_isstaff)

            # Guarda ambos registros
            profesional.save()
            user.save()

            # Si se ha subido una foto, al ultimo profesional añadido le pone
            # el DNI para identificarlo mejor, respetando la ruta "profesionales/<nombre>.<ext>"
            # Quedaría "profesionales/<dni>.<ext>"
            try:
                # Recupera el paciente grabado
                inter_profesional = Profesional.objects.get(pk = profesional.oto_Profesional)
                # Si se introduce un nombre de archivo
                split_name = str(inter_profesional.picturefile)
                if split_name != '':
                    # Trocea el nombre de la ruta por "/" y "."
                    # La parte del DNI es todo mayusculas
                    new_name = split_name.split('/')[0] + '/DNI_' + str(inter_profesional.dni).upper() + '.' + split_name.split('/')[1].split('.')[1].upper()
                    # Si ya existe un archivo con ese nombre lo borra antes de subir el nuevo
                    if Path(new_name).is_file():
                        os.remove(new_name)
                    # Sustituye al picture file original por el nuevo
                    inter_profesional.picturefile = new_name
                    # Limpia y guarda el registro
                    inter_profesional.save()
                    # Cambia el nombre del archivo en el disco
                    os.rename(str(settings.MEDIA_ROOT + '/' + split_name), str(settings.MEDIA_ROOT +'/' + new_name))   
            except:
                messages.warning(request, 'Error procesando archivo de imagen')

            return HttpResponseRedirect(reverse('id-profesionales', kwargs={'oto_Profesional': user.id}))
       
        else:
            messages.warning(request, 'El formularion contiene errores.')
            return render(request, 'create_profesionales_tpl.html', ctx)

        return render(request, 'create_profesionales_tpl.html', ctx)

    # GET
    def get(self, request, *args, **kwargs):
        
        # Si el usuario no es superuser no permite acceder a los datos
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))
            
        # Si esta autorizado asigna el form y sigue
        ctx = dict()
        form = create_edit_profesionales_form()
        ctx['form'] = form

        return render(request, 'create_profesionales_tpl.html', ctx)


@method_decorator(login_required, name='dispatch')
class edit_profesionales_view(View):

    def get(self, request):
    
        # Si el usuario no es superuser no permite acceder a los datos
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))

        return HttpResponseRedirect(reverse('error-privilegios-clinica'))

#############################################################