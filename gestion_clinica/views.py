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
from .forms import select_profesionales_form, create_profesionales_form, edit_profesionales_form, complete_profesionales_form
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

@method_decorator(login_required, name='dispatch')
class listado_profesionales_view(ListView):

    def get(self, request, **kwargs):

        ctx = dict()

        # Actua sobre la table de los usuarios User de django, y desde ahí accede a la tabla Profesional
        # Filtra el queryset de User y de Profesional
        qs = User.objects.all().select_related('profesionales').order_by('username')
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
    pk_url_kwarg = 'oto_Profesional'
    template_name = 'id_profesionales_tpl.html'

    def get_queryset(self):

        # Extrae el profesional en cuestion
        qs = Profesional.objects.select_related('oto_Profesional').filter(oto_Profesional__exact = self.kwargs['oto_Profesional'])

        return qs

@method_decorator(login_required, name='dispatch')
class create_profesionales_view(View):

    def get(self, request, *args, **kwargs):
        
        # Si el usuario no es superuser no permite acceder a los datos
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))
            
        # Si esta autorizado asigna el form y sigue
        ctx = dict()
        form = create_profesionales_form()
        ctx['form'] = form

        return render(request, 'create_profesionales_tpl.html', ctx)

    def post(self, request):

        # Si el usuario no es superuser no permite acceder a los datos
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))
  
        ctx = dict()
        
        # Pasa el fom al contexto
        form = create_profesionales_form(request.POST, request.FILES)
        ctx['form'] = form

        # Primero crea el User de django, para luego pasarlo a oto_Profesional y validar el form
        user_login = request.POST.get('user_login', '')
        user_password = request.POST.get('user_password', '')
        user_issuperuser = request.POST.get('user_issuperuser', False)
        user_isstaff = request.POST.get('user_isstaff', False)
        
        # Comprueba si existe ya ese usuario
        if User.objects.filter(username__exact = user_login).exists():
            messages.warning(request, 'El usuario ya existe.')
            return render(request, 'create_profesionales_tpl.html', ctx)
        # Si no existe lo crea
        else:
            user = User.objects.create_user(user_login, 'fixuSystem@email.usr', user_password)
            user.save()

        # Ahora valida el form
        if form.is_valid():

            # Pasa el form a un profesional
            profesional = form.save(commit = False)
            # Recupera el usuario creado
            user = User.objects.get(username__exact = user_login)

            # Pone el oto_Profesional
            profesional.oto_Profesional = user
            # Pone los campos que faltan de user: email, is active, is staff, is superuser
            user.email = profesional.email
            user.is_active = True
            user.is_superuser = bool(user_issuperuser)
            if user.is_superuser:
                user.is_staff = True                
            else:    
                user.is_staff = bool(user_isstaff)

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
            messages.warning(request, 'El formularion contiene errores')

            return render(request, 'create_profesionales_tpl.html', ctx)
        
        return HttpResponseRedirect(reverse('id-profesionales', kwargs={'oto_Profesional': user.id}))


@method_decorator(login_required, name='dispatch')
class complete_profesionales_view(View):
    
    def get(self, request, **kwargs):

        # Si el usuario no es superuser no permite acceder a los datos
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))
        
        # Si es superuser
        ctx = dict()

        # Recupera los datos de USER
        user_prof = int(self.kwargs['id'])
        user = User.objects.get(id__exact = user_prof)
        ctx['user_id'] = user.id

        # Inicia la form
        initial_data = {
            'user_login': user.username,
            'user_password': user.password,
            'user_isactive': user.is_active,
            'user_issuperuser': user.is_superuser,
            'user_isstaff': user.is_staff,
            'oto_Profesional': user.id
        }
        form = edit_profesionales_form(initial = initial_data)
        ctx['form'] = form

        return render(request, 'complete_profesionales_tpl.html', ctx)

    def post(self, request, **kwargs):

        # Si el usuario no es superuser no permite acceder a los datos
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))

        ctx = dict()
        
        # Pasa el form POST y FILES
        form = create_profesionales_form(request.POST, request.FILES)

        # Primero actualiza el User de django, para luego pasarlo a oto_Profesional
        # Recupera campos del POST
        user_id = request.POST.get('user_id')
        user_isactive = request.POST.get('user_isactive', False)
        user_issuperuser = request.POST.get('user_issuperuser', False)
        user_isstaff = request.POST.get('user_isstaff', False)
        user_email = request.POST.get('email', 'fixuSystem@email.usr')

        # Extrae el User
        user = User.objects.get(id__exact = user_id)

        # Ajusta los Is... y el email del User
        try:
            if bool(user_isactive):
                user.is_active = True
            else:
                user.is_active = False
            
            if bool(user_issuperuser):
                user.is_superuser = True
                user.is_staff = True
            else:
                user.is_superuser = False
                user.is_staff = bool(user_isstaff)
            user.email = user_email
            
            # Guarda User
            user.save()
        except:
            messages.warning(request, 'Error actualizando los datos de usuario/a')
            
            return HttpResponseRedirect(reverse('complete-profesionales', kwargs = {'id': user.id}))

        # Si va bien valida el form
        if form.is_valid():

            # Construye los 19 datos del modelo Profesional e INSERT el registro
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

            return HttpResponseRedirect(reverse('id-profesionales', kwargs={'oto_Profesional': user.id}))

        else:
            messages.warning(request, 'Error actualizando los datos del/de la profesional')

            return HttpResponseRedirect(reverse('complete-profesionales', kwargs = {'id': user.id}))

@method_decorator(login_required, name='dispatch')
class edit_profesionales_view(UpdateView):

    model = Profesional
    context_object_name = 'profesionales'
    pk_url_kwarg = 'oto_Profesional'
    form_class = edit_profesionales_form
    template_name = 'edit_profesionales_tpl.html'

    def get(self, request, *args, **kwargs):

        # Si el usuario no es superuser no permite acceder a los datos
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))
        else:
            return super().get(request, *args, **kwargs)

    def get_queryset(self):

        # Recupera el Profesional y User asociado
        qs = Profesional.objects.select_related('oto_Profesional').filter(oto_Profesional__exact = self.kwargs['oto_Profesional'])

        return qs

    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)

        # Recupera los datos de USER que son editables
        # is_active, is_superuser y is_staff
        user_prof = getattr(ctx['profesionales'], 'oto_Profesional')
        user = User.objects.get(username__exact = user_prof)
        ctx['user_'] = user
        
        return ctx

    def post(self, request, *args, **kwargs):

        # Si el usuario no es superuser no permite acceder a los datos
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('error-privilegios-clinica'))

        # Recupera del POST las keys que no se pasan en el form, referentes al User
        # Pone los datos de USER que son editables
        # is_active, is_superuser, is_staff y email
        user_id = int(request.POST.get('oto_Profesional')) 
        user_isactive = request.POST.get('user_isactive', False)
        user_issuperuser = request.POST.get('user_issuperuser', False)
        user_isstaff = request.POST.get('user_isstaff', False)
        user_email = request.POST.get('email', 'fixuSystem@email.usr')
        
        user = User.objects.get(id__exact = user_id)
        try:
            if bool(user_isactive):
                user.is_active = True
            else:
                user.is_active = False
            
            if bool(user_issuperuser):
                user.is_superuser = True
                user.is_staff = True
            else:
                user.is_superuser = False
                user.is_staff = bool(user_isstaff)
            
            user.email = user_email
            user.save()
        except:
            messages.warning(request, 'Error actualizando los datos de usuario/a')
            
            return HttpResponseRedirect(reverse('edit-profesionales', kwargs = {'oto_Profesional': user_id}))

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):

        # Pone los registros de control que faltan
        # Commit = False: evita que se guarde ya en la base de datos
        profesional = form.save(commit = False)
        # Campos de control
        if str(self.request.user) != 'AmonymousUser':
            profesional.modifiedby = str(self.request.user)
        else:
            profesional.modifiedby = 'unix:' + str(self.request.META['USERNAME'])
        # Limpia y guarda el registro
        profesional.save()
    
        # Si ha cambiado la foto
        # Si se actualiza la foto se renombra an DNI y se borra la antigua
        if 'picturefile' in form.changed_data:
            try:
                # Recupera el paciente grabado
                inter_profesional = Profesional.objects.get(oto_Profesional__exact = profesional.oto_Profesional.id)
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
                    
                return HttpResponseRedirect(reverse('id-profesionales', kwargs = {'oto_Profesional': profesional.oto_Profesional.id}))
            except:
                messages.warning(request, 'Error procesando archivo de imagen')
                
                return HttpResponseRedirect(reverse('edit-profesionales', kwargs = {'oto_Profesional': profesional.oto_Profesional.id}))
        else:

            return HttpResponseRedirect(reverse('id-profesionales', kwargs = {'oto_Profesional': profesional.oto_Profesional.id}))
