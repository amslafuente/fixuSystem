from django.shortcuts import render, reverse
from django.http import request, HttpResponseRedirect
from .forms import select_pacientes_form, create_edit_pacientes_form, select_edit_pacientes_form
from .models import Paciente
from django.views import View
from datetime import datetime
from django.views.generic import TemplateView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
import datetime
from django.conf import settings
import os
from pathlib import Path
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from fixuSystem.progfuncts import calculate_age



#########################################
#                                       #
#        MUESTRA ID DE PACIENTE         #
#                                       #
#########################################

@method_decorator(login_required, name='dispatch')
class id_pacientes_view(DetailView):

    model = Paciente
    context_object_name = 'pacientes'
    pk_url_kwarg = 'idPaciente'
    template_name = 'id_pacientes_tpl.html'

    def get_queryset(self):

        qs = Paciente.objects.filter(idPaciente__exact = self.kwargs['idPaciente'])
        return qs

    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)

        # Obtiene la edad a partir de la fecha de nacimiento
        bd = getattr(ctx['pacientes'], 'birthdate')
        # Calcula la diferencia entre bd y el dia de hoy
        age = calculate_age(bd)
        ctx['age'] = age
        # Prepara en el contexto la fecha actual para pasarla como DESDE_FECHA para las citas de este paciente
        ctx['desde_fecha'] = datetime.date.today().strftime('%d_%m_%Y')
        return ctx



#########################################
#                                       #
#   CREACION Y EDICION DE DE PACIENTES  #
#                                       #
#########################################

@method_decorator(login_required, name='dispatch')
class create_pacientes_view(CreateView):

    model = Paciente
    context_object_name = 'pacientes'
    form_class = create_edit_pacientes_form
    pk_url_kwarg = 'idPaciente'
    template_name = 'create_edit_pacientes_tpl.html'
    
    def form_valid(self, form):

        # Pone los registros de control que faltan en una instancia "manejable": paciente
        # Commit = False: evita que se guarde ya en la base de datos
        paciente = form.save(commit = False)
        # Campos de control
        if str(self.request.user) != 'AmonymousUser':
            paciente.modifiedby = str(self.request.user)
        else:
            paciente.modifiedby = 'unix:' + str(self.request.META['USERNAME'])
        paciente.save()

        # Si se ha subido una foto, al ultimo paciente  añadido le pone
        # el DNI para identificarlo mejor, respetando la ruta "pacientes/<nombre>.<ext>"
        # Quedaría "pacientes/<dni>.<ext>"
        try:
            # Recupera el paciente grabado
            paciente = Paciente.objects.get(idPaciente__exact = paciente.idPaciente)
            # Si se introduce un nombre de archivo
            split_name = str(paciente.picturefile)
            if split_name != '':
                # Trocea el nombre de la ruta por "/" y "."
                # La parte del DNI es todo mayusculas
                new_name = split_name.split('/')[0] + '/DNI_' + str(inter_paciente.dni).upper() + '.' + split_name.split('/')[1].split('.')[1].upper()
                # Si ya existe un archivo con ese nombre lo borra antes de subir el nuevo
                if Path(new_name).is_file():
                    os.remove(new_name)
                # Sustituye al picture file original por el nuevo
                paciente.picturefile = new_name
                # Limpia y guarda el registro
                paciente.save()
                # Cambia el nombre del archivo en el disco
                os.rename(str(settings.MEDIA_ROOT + '/' + split_name), str(settings.MEDIA_ROOT +'/' + new_name))   
        except:
            messages.warning(request, 'Error procesando archivo de imagen')
        
        return HttpResponseRedirect(reverse('id-pacientes', kwargs={'idPaciente': paciente.idPaciente}))

@method_decorator(login_required, name='dispatch')
class edit_pacientes_view(UpdateView):

    model = Paciente
    context_object_name = 'paciente'
    pk_url_kwarg = 'idPaciente'
    template_name = 'create_edit_pacientes_tpl.html'
    form_class = create_edit_pacientes_form

    # Arregla el contexto y pasa idPaciente al template
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        # Coge el registro de ese paciente
        context["idPaciente"] = self.kwargs['idPaciente']
        
        return context

    # Actualiza el campo modifiedby y la foto
    def form_valid(self, form):

        # Pone los registros de control que faltan en una instancia "manejable": paciente
        # Commit = False: evita que se guarde ya en la base de datos
        paciente = form.save(commit = False)
        #Campos de control
        if str(self.request.user) != 'AmonymousUser':
            paciente.modifiedby = str(self.request.user)
        else:
            paciente.modifiedby = 'unix:' + str(self.request.META['USERNAME'])
        # Limpia y guarda el registro
        paciente.save()

        # Si se actualiza la foto se renombra an DNI y se borra la antigua
        if 'picturefile' in form.changed_data:
            picture_changed = True
        else:
            picture_changed = False
        if picture_changed:
            try:
                # Recupera el paciente grabado
                inter_paciente = Paciente.objects.get(pk = paciente.idPaciente)
                # Si se introduce un nombre de archivo
                split_name = str(inter_paciente.picturefile)
                if split_name != '':
                    # Trocea el nombre de la ruta por "/" y "."
                    # La parte del DNI es todo mayusculas
                    new_name = split_name.split('/')[0] + '/DNI_' + str(inter_paciente.dni).upper() + '.' + split_name.split('/')[1].split('.')[1].upper()
                    # Si ya existe un archivo con ese nombre lo borra antes de subir el nuevo
                    if Path(new_name).is_file():
                        os.remove(new_name)
                    # Sustituye al picture file original por el nuevo
                    inter_paciente.picturefile = new_name
                    # Limpia y guarda el registro
                    inter_paciente.save()
                    # Cambia el nombre del archivo en el disco
                    os.rename(str(settings.MEDIA_ROOT + '/' + split_name), str(settings.MEDIA_ROOT +'/' + new_name))
            except:

                messages.warning(request, 'Error procesando archivo de imagen')

        return HttpResponseRedirect(reverse('id-pacientes', kwargs = {'idPaciente' : paciente.idPaciente}))



#########################################
#                                       #
#        LISTADO DE PACIENTES           #
#                                       #
#########################################

@method_decorator(login_required, name='dispatch')
class listado_pacientes_view(ListView):

    model = Paciente
    context_object_name = 'pacientes'
    template_name = 'listado_pacientes_tpl.html'
    paginate_by = 20

    def get_queryset(self):

        qs = super().get_queryset()

        # Seleccion
        if self.kwargs['dni'] != 'dni':
            qs = qs.filter(dni__icontains = self.kwargs['dni'])
        if self.kwargs['name'] != 'nombre':
             qs = qs.filter(name__icontains = self.kwargs['name'])
        if self.kwargs['familyname'] != 'apellidos':
             qs = qs.filter(familyname__icontains = self.kwargs['familyname'])
        # ORDERBY de los campos y registros
        if self.kwargs['orderby'] == 'A':
             qs = qs.order_by('familyname').values('idPaciente', 'dni', 'familyname', 'name')
        elif self.kwargs['orderby'] == 'N':
             qs = qs.order_by('name').values('idPaciente', 'dni', 'name', 'familyname')
        elif self.kwargs['orderby'] == 'D':
             qs = qs.order_by('dni').values('idPaciente', 'dni', 'name', 'familyname')
        else:
             qs = qs.order_by('idPaciente').values('idPaciente', 'dni', 'name', 'familyname')

        return qs

    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)
        # Pasa la fecha de hoy para crear el enlace a las citas pendientes
        ctx['desde_fecha'] = datetime.date.today().strftime('%d_%m_%Y')
        # Pasa la ordenacion de la lista de pacientes
        ctx['head_order'] = self.kwargs['orderby']
        return ctx



#########################################
#                                       #
#   VIEWS PARA SELECCION DE PACIENTES   #
#                                       #
#########################################

# View para seleccionar pacientes a listar
@method_decorator(login_required, name='dispatch')
class select_pacientes_view(View):

    def get(self, request):

        ctx = dict()
        # Limpia el form y lo añade al contexto
        form = select_pacientes_form()
        ctx['form'] = form        
        return render(request, 'select_pacientes_tpl.html', ctx)

    def post(self, request):

        ctx = dict()
        form = select_pacientes_form(request.POST)

        if form.is_valid():
            # Devuelve las partes que interesan en una string para mostrar solo esos pacientes
            show_str = {'dni':'dni', 'name':'nombre', 'familyname':'apellidos', 'orderby':'A'}
            if str(form.cleaned_data['dni']) != '':
                show_str['dni'] = form.cleaned_data['dni']
            if str(form.cleaned_data['name']) != '':
                show_str['name'] = form.cleaned_data['name']
            if str(form.cleaned_data['familyname']) != '':
                show_str['familyname'] = form.cleaned_data['familyname']
            show_str['orderby'] = form.cleaned_data['orderby']
            return HttpResponseRedirect(reverse('listado-pacientes', kwargs = show_str))
        else:
            form = select_pacientes_form()
            ctx['form'] = form
            messages.warning(request, 'El formulario contiene errores')
            return render(request, 'select_pacientes_tpl.html', ctx)

# View para seleccionar pacientes a editar
@method_decorator(login_required, name='dispatch')
class select_edit_pacientes_view(View):

    def get(self, request):

        ctx = dict()
        # Limpia el form y lo añade al contexto
        form = select_edit_pacientes_form()
        ctx['form'] = form
        return render(request, 'select_edit_pacientes_tpl.html', ctx)

    def post(self, request):

        ctx = dict()
        form = select_edit_pacientes_form(request.POST)

        if form.is_valid():
            show_str = dict()

            # Si devuelve un id comprueba que existe y pasa a edicion...
            if form.cleaned_data['idpac'] != '':
                # Filtra ese id convirtiendolo a numero si se puede
                try:
                    idpac = int(form.cleaned_data['idpac'])
                    existe_id = Paciente.objects.filter(idPaciente__exact = idpac).exists()
                except ValueError:
                    idpac = 0
                    existe_id = False

                # Si existe...
                if existe_id:
                    show_str['idPaciente'] = idpac
                    return HttpResponseRedirect(reverse('edit-pacientes', kwargs = show_str))
                # Si no existe pasa a seleccion general
                else:
                    messages.warning(request, 'No existe esa ID - Use la búsqueda ampliada')
                    return HttpResponseRedirect(reverse('select-pacientes'))

            # Si devuevle un DNI, recupera el registro y lee el id para pasarlo...
            elif form.cleaned_data['dni'] != '':
                # Filtra ese DNI
                dnipac = form.cleaned_data['dni']
                existe_dni = Paciente.objects.filter(dni__iexact = dnipac).exists()
                
                # Si existe...
                if existe_dni:
                    show_str['idPaciente'] = dnipac
                    return HttpResponseRedirect(reverse('edit-pacientes', kwargs = show_str))

                # Si no existe pasa a seleccion general
                else:
                    messages.warning(request, 'No existe ese DNI - Use la búsqueda ampliada')
                    return HttpResponseRedirect(reverse('select-pacientes'))
            # Si no marca nada manda a la ventana select general
            else:
                return HttpResponseRedirect(reverse('select-pacientes'))

        # El form NO es validado
        else:
            # Limpia el form y añade al contexto
            form = select_edit_pacientes_form()
            ctx['form'] = form
            messages.warning(request, 'El formulario contiene errores')
            return render(request, 'select_edit_pacientes_tpl.html', ctx)

