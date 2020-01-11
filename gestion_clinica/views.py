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
from django.db.models import Q

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

# Error si el usuario NO ES SUPERUSUARIO
@method_decorator(login_required, name='dispatch')
class error_privilegios_clinica_view(TemplateView):
    template_name = 'error_privilegios_clinica_tpl.html'

# Error si el usuario NO ES SUPERUSUARIO
@method_decorator(login_required, name='dispatch')
class error_profesionales_clinica_view(TemplateView):
    template_name = 'error_privilegios_profesionales_tpl.html'

# Error si el usuario ES ROOT
@method_decorator(login_required, name='dispatch')
class error_root_clinica_view(TemplateView):
    template_name = 'error_root_tpl.html'

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

    # GET al llamar a la view
    def get(self, request):

        # Si el usuario no es o staff no permite acceder a los datos de la clinica
        if (not request.user.is_superuser) and (not request.user.is_staff):
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))

        return super().get(request)

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
    
    def get(self, request, **kwargs):

        # Si el usuario no es o staff no permite acceder a los datos de la clinica
        if (not request.user.is_superuser) or (not request.user.is_staff):
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))

        return super().get(request)

    def get_queryset(self):

        # Extrae el consultorio en cuestion
        qs = Consultorio.objects.filter(idConsultorio__exact = self.kwargs['idConsultorio'])

        return qs

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
    
    def get(self, request):

        # Si el usuario no es o staff no permite acceder a los datos de la clinica
        if (not request.user.is_superuser) and (not request.user.is_staff):
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))

        return super().get(request)
    
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


@method_decorator(login_required, name='dispatch')
class edit_equipamiento_view(UpdateView): 

    model = Equipamiento
    context_object_name = 'equipamiento'
    pk_url_kwarg = 'idEquipamiento'
    form_class = create_edit_equipamiento_form
    template_name = 'edit_equipamiento_tpl.html'

    def get(self, request, **kwargs):

        # Si el usuario no es o staff no permite acceder a los datos de la clinica
        if (not request.user.is_superuser) or (not request.user.is_staff):
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))

        return super().get(request)

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

@method_decorator(login_required, name='dispatch')
class delete_equipamiento_view(DeleteView):

    model = Equipamiento
    context_object_name = 'equipamientos'
    pk_url_kwarg = 'idEquipamiento'
    template_name = 'delete_equipamiento_tpl.html'
    success_url = reverse_lazy('listado-equipamiento')

    def get(self, request, **kwargs):

        # Si el usuario no es o staff no permite acceder a los datos de la clinica
        if (not request.user.is_superuser) or (not request.user.is_staff):
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))

        return super().get(request)
    
    def get_queryset(self):
    
        # Extrae el consultorio en cuestion
        qs = Equipamiento.objects.filter(idEquipamiento__exact = self.kwargs['idEquipamiento'])

        return qs

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
    
    def get(self, request):

        # Si el usuario no es o staff no permite acceder a los datos de la clinica
        if (not request.user.is_superuser) and (not request.user.is_staff):
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))

        return super().get(request)

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
        
        messages.warning(self.request, 'Errores en el formulario')
        
        return super().form_invalid(form)

@method_decorator(login_required, name='dispatch')
class edit_proveedores_view(UpdateView):

    model = Proveedor
    context_object_name = 'proveedores'
    pk_url_kwarg = 'idProveedor'
    form_class = create_edit_proveedores_form
    template_name = 'edit_proveedores_tpl.html'

    def get(self, request, **kwargs):

        # Si el usuario no es o staff no permite acceder a los datos de la clinica
        if (not request.user.is_superuser) or (not request.user.is_staff):
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))

        return super().get(request)

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

@method_decorator(login_required, name='dispatch')
class delete_proveedores_view(DeleteView):

    model = Proveedor
    context_object_name = 'proveedores'
    pk_url_kwarg = 'idProveedor'
    template_name = 'delete_proveedores_tpl.html'
    success_url = reverse_lazy('listado-proveedores')

    def get(self, request, **kwargs):

        # Si el usuario no es o staff no permite acceder a los datos de la clinica
        if (not request.user.is_superuser) or (not request.user.is_staff):
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))

        return super().get(request)

    def get_queryset(self):
    
        # Extrae el consultorio en cuestion
        qs = Proveedor.objects.filter(idProveedor__exact = self.kwargs['idProveedor'])

        return qs

##################################################
#                   PROFESIONALES                #
##################################################

##### ID DE PROFESIONALES #####

@method_decorator(login_required, name='dispatch')
class profesionales_clinica_view(TemplateView):

    template_name = 'profesionales_clinica_tpl.html'

    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)
        ctx['id'] = self.request.user.id
        return ctx

##### SELECCIONA Y MUESTRA PROFESIONALES #####

@method_decorator(login_required, name='dispatch')
class select_profesionales_view(View):

    def get(self, request):

        ctx = dict()
        # Limpia el form y lo añade al contexto
        form = select_profesionales_form()
        ctx['form'] = form        
        return render(request, 'select_profesionales_tpl.html', ctx)

    def post(self, request):

        ctx = dict()
        # Rellena el form con el POST y añade al contexto
        form = select_profesionales_form(request.POST)

        # El form SI es validado
        if form.is_valid():
            # Devuelve las partes que interesan en una string para mostrar solo esos profesionales
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

@method_decorator(login_required, name='dispatch')
class listado_profesionales_view(ListView):

    def get(self, request, **kwargs):

        ctx = dict()
        # Actua sobre la tabla de los usuarios User de django, y desde ahí accede a la tabla Profesional
        # Filtra el queryset de User y de Profesional
        # EXCLUYE al usuario ROOT por consistencia con los sistemas unix
        qs = User.objects.all().select_related('profesionales').exclude(username__iexact = 'root').order_by('profesionales__fullname')
        # Seleccion
        if kwargs['fullname'] != 'fullname':
            qs_user = Q(username__icontains = kwargs['fullname'])
            qs_profesional = Q(profesionales__fullname__icontains = kwargs['fullname'])
            qs = qs.filter(qs_user | qs_profesional)
        if kwargs['position'] != 'position':
             qs = qs.filter(profesionales__position__icontains = kwargs['position'])
        if kwargs['department'] != 'department':
             qs = qs.filter(profesionales__department__icontains = kwargs['department'])
        ctx['profesionales'] = qs
        return render(request, 'listado_profesionales_tpl.html', ctx)

@method_decorator(login_required, name='dispatch')
class id_profesionales_view(DetailView):

    model = Profesional
    context_object_name = 'profesionales'
    pk_url_kwarg = 'id'
    template_name = 'id_profesionales_tpl.html'

    def get(self, request, *args, **kwargs):

        # Comprueba si los datos de ese Profesional están completos (si no existe no lo están)
        existe = Profesional.objects.filter(oto_Profesional__exact = self.kwargs['id']).exists()
        if not existe:
            messages.warning(self.request, 'Los datos de este/a profesional están incompletos')
            return HttpResponseRedirect(reverse('complete-profesionales', kwargs = {'id': self.kwargs['id']}))
        else:
            return super().get(request, *args, **kwargs)

    def get_queryset(self):

        # Extrae el profesional en cuestion
        qs = Profesional.objects.select_related('oto_Profesional').filter(oto_Profesional__exact = self.kwargs['id'])
        return qs

##### CREA Y EDITA PROFESIONALES #####

@method_decorator(login_required, name='dispatch')
class create_profesionales_view(View):

    def get(self, request, *args, **kwargs):
        
        # Si el usuario no es superuser no permite acceder a los datos
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('error-privilegios-profesionales'))
            
        # Si esta autorizado asigna el form y sigue
        ctx = dict()
        form = create_edit_profesionales_form()
        ctx['form'] = form
        return render(request, 'create_profesionales_tpl.html', ctx)

    def post(self, request):

        # Si el usuario no es superuser no permite acceder a los datos
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('error-privilegios-profesionales'))
  
        ctx = dict()        
        # Pasa el fom al contexto
        form = create_edit_profesionales_form(request.POST, request.FILES)
        ctx['form'] = form

        # Primero crea el User de django, para luego pasarlo a oto_Profesional y validar el form
        user_login = request.POST.get('user_login')
        user_password = request.POST.get('user_password')
        
        # Comprueba si existe ya ese usuario
        if User.objects.filter(username__exact = user_login).exists():
            messages.warning(request, 'Este/a usuario/a ya existe')            
            return render(request, 'create_profesionales_tpl.html', ctx)
        # Si no existe lo crea
        else:
            user = User.objects.create_user(username = user_login, email = 'fixuSystem@email.usr', password = user_password)

        # Valida
        if form.is_valid():
            profesional = form.save(commit = False)
            # Recupera el usuario creado y pone oto_Profesional
            user = User.objects.get(username__exact = user_login)
            profesional.oto_Profesional = user
            # Pone los campos que faltan de user: email, is active, is staff, is superuser
            user.email = form.cleaned_data['email']
            user.is_active = form.cleaned_data['user_isactive']
            user.is_superuser = form.cleaned_data['user_issuperuser']
            user.is_staff = form.cleaned_data['user_isstaff']
            # Guarda ambos registros
            profesional.save()
            user.save()

            # Si se ha subido una foto, al ultimo profesional añadido le pone
            # el DNI para identificarlo mejor, respetando la ruta "profesionales/<nombre>.<ext>"
            # Quedaría "profesionales/<dni>.<ext>"
            try:
                # Recupera el paciente grabado
                profesional = Profesional.objects.get(oto_Profesional__exact = user.id)
                # Si se introduce un nombre de archivo
                split_name = str(profesional.picturefile)
                if split_name != '':
                    # Trocea el nombre de la ruta por "/" y "."
                    # La parte del DNI es todo mayusculas
                    new_name = split_name.split('/')[0] + '/DNI_' + str(profesional.dni).upper() + '.' + split_name.split('/')[1].split('.')[1].upper()
                    # Si ya existe un archivo con ese nombre lo borra antes de subir el nuevo
                    if Path(new_name).is_file():
                        os.remove(new_name)
                    # Sustituye al picture file original por el nuevo
                    profesional.picturefile = new_name
                    # Limpia y guarda el registro
                    profesional.save()
                    # Cambia el nombre del archivo en el disco
                    os.rename(str(settings.MEDIA_ROOT + '/' + split_name), str(settings.MEDIA_ROOT +'/' + new_name))   
            except:
                messages.warning(request, 'Error procesando archivo de imagen')
                return render(request, 'create_profesionales_tpl.html', ctx)    
            return HttpResponseRedirect(reverse('id-profesionales', kwargs = {'id': user.id}))
        else:
            messages.warning(request, 'El formularion contiene errores')
            return render(request, 'create_profesionales_tpl.html', ctx)        

@method_decorator(login_required, name='dispatch')
class complete_profesionales_view(View):
    
    def get(self, request, **kwargs):

        # Si el usuario no es superuser o no es propio usuario no permite acceder a los datos
        if (not request.user.is_superuser) and (request.user.id != self.kwargs['id']):
            return HttpResponseRedirect(reverse('error-privilegios-profesionales'))
        
        # Si es superuser
        ctx = dict()
        # Recupera los datos de USER
        user = User.objects.get(id__exact = self.kwargs['id'])  
        
        # Si el usuario es ROOT no se toca, por consistencia con el usuario de unix
        if user.username.upper() == 'ROOT':
            return HttpResponseRedirect(reverse('error-root'))     
        # Si no es root continua
        ctx['user_id'] = user.id
        ctx['user_login'] = user.username
        ctx['user_password'] = user.password

        # Inicia la form con los datos del User. Los del Profesional están en blanco.
        initial_data = {
            'user_isactive': user.is_active,
            'user_issuperuser': user.is_superuser,
            'user_isstaff': user.is_staff,
            'oto_Profesional': user.id
        }
        form = create_edit_profesionales_form(initial = initial_data)
        ctx['form'] = form

        return render(request, 'complete_profesionales_tpl.html', ctx)

    def post(self, request, **kwargs):

        # Si el usuario no es superuser o no es propio usuario no permite acceder a los datos
        if (not request.user.is_superuser) and (request.user.id != self.kwargs['id']):
            return HttpResponseRedirect(reverse('error-privilegios-profesionales'))

        ctx = dict()        
        # Pasa el form POST y FILES
        form = create_edit_profesionales_form(request.POST, request.FILES)

        # Valida el form
        if form.is_valid():
            # Extrae el User
            user = User.objects.get(id__exact = self.kwargs['id'])
            # Cambia los is_...
            user.is_active = form.cleaned_data['user_isactive']
            user.is_superuser = form.cleaned_data['user_issuperuser']
            if user.is_superuser:
                user.is_staff = True
            else:
                user_isstaff = form.cleaned_data['user_isstaff']
            # Cambia el email_...
            user.email = form.cleaned_data['email']
            user.save()

            # Ahora construye los 19 datos del modelo Profesional e INSERT el registro
            profesional = Profesional(
                oto_Profesional = user,
                dni = form.cleaned_data['dni'],
                nif = form.cleaned_data['nif'],
                fullname = form.cleaned_data['fullname'],
                numcolegiado = form.cleaned_data['numcolegiado'],
                position = form.cleaned_data['position'],
                department = form.cleaned_data['department'],
                fulladdress = form.cleaned_data['fulladdress'],
                postcode = form.cleaned_data['postcode'],
                city = form.cleaned_data['city'],
                province = form.cleaned_data['province'],
                country = form.cleaned_data['country'],
                email = form.cleaned_data['email'],
                phone1 = form.cleaned_data['phone1'],
                phone2 = form.cleaned_data['phone2'],
                currentavail = form.cleaned_data['currentavail'],
                currentstaff = form.cleaned_data['currentstaff'],
                picturefile = form.cleaned_data['picturefile'],
                notes = form.cleaned_data['notes'],
                modifiedby = 'fixuUser'
            )
            profesional.save()

            # Campos de control
            profesional = Profesional.objects.get(oto_Profesional__exact = user.id)
            if str(self.request.user) != 'AmonymousUser':
                profesional.modifiedby = str(self.request.user)
            else:
                profesional.modifiedby = 'unix:' + str(self.request.META['USERNAME'])
    
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
            return HttpResponseRedirect(reverse('id-profesionales', kwargs={'id': user.id}))

        else:
            messages.warning(request, 'Error actualizando los datos del/de la profesional')
            return HttpResponseRedirect(reverse('complete-profesionales', kwargs = {'id': self.kwargs['id']}))

@method_decorator(login_required, name='dispatch')
class edit_profesionales_view(UpdateView):

    model = Profesional
    context_object_name = 'profesionales'
    pk_url_kwarg = 'id'
    form_class = create_edit_profesionales_form
    template_name = 'edit_profesionales_tpl.html'

    def get(self, request, *args, **kwargs):
    
        # Si el usuario no es superuser o no es propio usuario no permite acceder a los datos
        if (not request.user.is_superuser) and (request.user.id != self.kwargs['id']):
            return HttpResponseRedirect(reverse('error-privilegios-profesionales'))
        else:
            return super().get(request, *args, **kwargs)

    def get_queryset(self):

        # Recupera el registro del Profesional a editar
        qs = Profesional.objects.select_related('oto_Profesional').filter(oto_Profesional__exact = self.kwargs['id'])
        return qs

    def get_context_data(self, **kwargs):

        # Pasa User login, id y password al contexto
        ctx = super().get_context_data(**kwargs)
        profesional = ctx['profesionales']
        user = getattr(profesional, 'oto_Profesional')
        ctx['user_login'] = user.username
        ctx['user_id'] = user.id
        ctx['user_password'] = user.password
        return ctx
    
    def get_initial(self):

        initial = super().get_initial()
        # Ponee los valores iniciales de los campos user.is_... del User
        user = User.objects.get(id__exact = self.kwargs['id']) 
        if user.is_superuser:
            user.is_staff = True       
        initial = {    
            'user_issuperuser': user.is_superuser,
            'user_isstaff': user.is_staff,            
            'user_isactive': user.is_active,            
        }
        return initial

    def post(self, request, *args, **kwargs):

        # Si el usuario no es superuser o no es propio usuario no permite acceder a los datos
        if (not request.user.is_superuser) and (request.user.id != self.kwargs['id']):
            return HttpResponseRedirect(reverse('error-privilegios-profesionales'))

        # Actualiza el user.is_... y el user.email
        user = User.objects.get(id__exact = request.POST.get('user_id'))
        user.is_active = bool(request.POST.get('user_isactive')) 
        user.is_superuser = bool(request.POST.get('user_issuperuser'))
        if user.is_superuser:
            user.is_staff = True
        else:
            user.is_staff = bool(request.POST.get('user_isstaff'))
        user.email = request.POST.get('email')
        user.save()
        return super().post(request, *args, **kwargs)

##### CAMBIA CLAVE PROFESIONALES #####

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

@method_decorator(login_required, name='dispatch')
class id_clave_profesionales_view(View):

    def get(self, request, **kwargs):

        ctx = dict()        
        # Si es superuser permite cambiar cualquier usuario
        # Si no es superuser solo permite que se cambie a si mismo
        if request.user.is_superuser:
            user_ = User.objects.get(id__exact = self.kwargs['id'])
        elif request.user.id == self.kwargs['id']:
            user_ = User.objects.get(id__exact = request.user.id)                    
        else:
            return HttpResponseRedirect(reverse('error-privilegios-profesionales'))
      
        # Pasa en usuario
        form = PasswordChangeForm(user_)
        ctx['form'] = form
        return render(request, 'id_clave_profesionales_tpl.html', ctx)

    def post(self, request, **kwargs):

        ctx = dict()
        # Recupera el form, pero... OJO al usuario
        # Este el el usuario cambiado, que puede ser diferente de request.user
        user_ = User.objects.get(id__exact = self.kwargs['id'])
        form = PasswordChangeForm(user_, request.POST) # Ese user NO es el correcto, hay que cogerlo de self.kwargs['id'])
        ctx['form'] = form
        
        if form.is_valid():
            user_ = form.save()
            update_session_auth_hash(request, user_)  # Importante!
            return HttpResponseRedirect(reverse('id-profesionales', kwargs = {'id': self.kwargs['id']}))
        else:
            messages.warning(request, 'Errores en el formulario')
        return render(request, 'id_clave_profesionales_tpl.html', ctx)