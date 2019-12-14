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
from .models import Clinica, Profesional, Consultorio
from .forms import init_edit_info_clinica_form, create_edit_consultorios_form
import os
from pathlib import Path
from django.conf import settings

########## MUESTRA DATOS DE CLINICA ##########

@method_decorator(login_required, name='dispatch')
class info_clinica_view(View):

    def get(self, request):

        # Recupera el primer registro encontrado, que es el que vale
        qs = Clinica.objects.first()
        ctx = dict()
        ctx['clinica'] = qs
        return render (request, 'info_clinica_tpl.html', ctx)

    def form_valid(self, form):

        pass


########## INICIALIZA DATOS DE CLINICA ##########

@method_decorator(login_required, name='dispatch')
class init_clinica_view(View):

    # POST al volver del formulario
    def post(self, request):

        # Se meten los datos del formulario
        ctx= dict()
        form = init_edit_info_clinica_form(request.POST, request.FILES)
        ctx['form'] = form

        # Si el formulario es valido
        if form.is_valid():

            # Almacena temporalmente
            clinica = form.save(commit = False)

            # firstupdated y last updaetd se ponen automaticamente

            # Pone modifiedby
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

                # Recupera el paciente grabado
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

            # Regresa a mostar los datos
            return HttpResponseRedirect(reverse('info-clinica'))

        # Si la form no es valida recarga co  los errores
        else:

            # mensajes de error
            messages.warning(request, 'Errores en el formulario')

            # Regresa al formulario
            return render(request, 'init_info_clinica_tpl.html', ctx)

    # GET al llamar a la view
    def get(self, request):

        # Cuenta los registros de la base de datos Clinica
        qs_count = Clinica.objects.count()

        # Si el usuario no es superuser no permite acceder a los datos de la clinica
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('error-init-usuario'))

        # Si ya existe un registro avisa de que solo se puede editar, no crear
        elif qs_count > 0:
            return HttpResponseRedirect(reverse('error-init-clinica'))

        # Si no existe pasa a crearlo
        else:

            # Inicia contexto
            ctx = dict()

            # Asocia la form y la pasa al contexto
            form = init_edit_info_clinica_form()
            ctx['form'] = form

            # Regresa al formulario
            return render(request, 'init_info_clinica_tpl.html', ctx)

# Error si el usuario NO ES SUPERUSUARIO
@method_decorator(login_required, name='dispatch')
class error_init_usuario_view(TemplateView):

    template_name = 'error_init_usuario_tpl.html'

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

        self.object = self.get_object()

        # Si no es superusuario no permite acceder a los datos de clinica
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('error-init-usuario'))
        else:
            return super().get(request, *args, **kwargs)

    # Actualiza el campo modifiedby y la foto
    def form_valid(self, form):

        # Sobre la form en bruto se determina si se ha cambiado el logo
        picture_changed = False
        if 'picturefile' in form.changed_data:
            picture_changed = True

        # Pone los registros de control que faltan en una instancia "manejable": paciente
        # Commit = False: evita que se guarde ya en la base de datos
        clinica = form.save(commit = False)

        # Los campos firstupdated y lastupdated se añaden solos

        # Se pone modifiedby
        if str(self.request.user) != 'AmonymousUser':
            clinica.modifiedby = str(self.request.user)
        else:
            clinica.modifiedby = 'unix:' + str(self.request.META['USERNAME'])

        # Limpia y guarda el registro
        clinica.save()

        # Si se actualiza el logo se renombra a 'logo-clinica' (sin extension) y se borra el antiguo
        if picture_changed:

            try:
                # Recupera el paciente grabado
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

        # Devuelve la form
        return HttpResponseRedirect(reverse('info-clinica'))

########## MUESTRA MENU DE GESTION DE SERVICIOS ##########

@method_decorator(login_required, name='dispatch')
class instalac_servic_clinica_view(TemplateView):

    template_name = 'instalac_servic_clinica_tpl.html'

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
    paginate_by = 25
    template_name = 'listado_consultorios_tpl.html'

    def get_queryset(self):

        # Todos los consultorios ordenados por officeID
        qs = Consultorio.objects.all().order_by('officeID')
        return qs


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

        # Los campos firstupdated y lastupdated se añaden solos

        # Se pone modifiedby
        if str(self.request.user) != 'AmonymousUser':
            consultorio.modifiedby = str(self.request.user)
        else:
            consultorio.modifiedby = 'unix:' + str(self.request.META['USERNAME'])

        # Limpia y guarda el registro
        consultorio.save()

        # Regresa a mostrar el consultorio nuevo
        return HttpResponseRedirect(reverse('listado-consultorios'))

    # GET al llamar a la view
    def get(self, request):

        # Si el usuario no es o staff no permite acceder a los datos de la clinica
        if (not request.user.is_superuser) and (not request.user.is_staff):
            return HttpResponseRedirect(reverse('error-consultorios-usuario'))

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
            return HttpResponseRedirect(reverse('error-consultorios-usuario'))

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
            return HttpResponseRedirect(reverse('error-consultorios-usuario'))

        return super().get(request)

# Error si el usuario NO ES SUPERUSUARIO
@method_decorator(login_required, name='dispatch')
class error_consultorios_usuario_view(TemplateView):

    template_name = 'error_consultorios_usuario_tpl.html'

#############################################################


@method_decorator(login_required, name='dispatch')
class profesionales_clinica_view(View):

    pass
