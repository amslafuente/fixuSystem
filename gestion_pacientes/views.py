from django.shortcuts import render, reverse
from django.http import request, HttpResponseRedirect
from .forms import select_pacientes_form, create_pacientes_form
from .forms import edit_pacientes_form, edit_id_pacientes_form
from .models import Paciente
from django.views import View
from datetime import datetime
from django.views.generic import TemplateView
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

########## CREATE PACIENTES VIEW ##########

@method_decorator(login_required, name='dispatch')
class create_pacientes_view(View):

    def post(self, request):
        ctx = dict()
        # Rellena el form con el POST y la añade  al contexto
        form = create_pacientes_form(request.POST, request.FILES)
        ctx['form'] = form

        # El form SI es validado
        if form.is_valid():

            # Pone los registros de control que faltan en una instancia "manejable": paciente
            # Commit = False: evita que se guarde ya en la base de datos
            paciente = form.save(commit = False)

            # Los campos firstupdated y lastupdated se añaden solos

            # Se pone modifiedby
            if str(request.user) != 'AmonymousUser':
                paciente.modifiedby = str(request.user)
            else:
                paciente.modifiedby = 'unix:' + str(request.META['USERNAME'])

            # Limpia y guarda el registro
            paciente.save()

            # Si se ha subido una foto, al ultimo paciente  añadido le pone
            # el DNI para identificarlo mejor, respetando la ruta "pacientes/<nombre>.<ext>"
            # Quedaría "pacientes/<dni>.<ext>"
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
            
            return HttpResponseRedirect(reverse('id-pacientes', kwargs={'idPaciente': paciente.idPaciente}))

        # El form NO es validado
        else:
            return render(request, 'create_pacientes_tpl.html', ctx)

    def get(self, request):
        ctx = dict()
        # El form limpio lo añade al contexto
        form = create_pacientes_form()
        ctx['form'] = form
        return render(request, 'create_pacientes_tpl.html', ctx)

########## SELECT PACIENTES VIEW ##########

@method_decorator(login_required, name='dispatch')
class select_pacientes_view(View):

    # POST
    def post(self, request):

        ctx = dict()
        # Rellena el form con el POST y añade al contexto
        form = select_pacientes_form(request.POST)
        ctx['form'] = form

        # El form SI es validado
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

        # El form NO es validado
        else:
            # Limpia el form y añade al contexto
            form = select_pacientes_form()
            ctx['form'] = form

            # Mensaje de error en contexto
            messages.warning(request, 'El formulario contiene errores')

            return render(request, 'select_pacientes_tpl.html', ctx)

    # GET
    def get(self, request):
        ctx = dict()
        # Limpia el form y lo añade al contexto
        form = select_pacientes_form()
        ctx['form'] = form
        return render(request, 'select_pacientes_tpl.html', ctx)

########## SHOW PACIENTES VIEW ##########

@method_decorator(login_required, name='dispatch')
class listado_pacientes_view(ListView):

    model = Paciente
    context_object_name = 'pacientes'
    template_name = 'listado_pacientes_tpl.html'
    paginate_by = 20

    # Modifica el query ALL para seleccionar los pacientes elegidos
    def get_queryset(self):

        # Filtrado del query por defecto
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

    # Añade las cabeceras de la tabla al contexto y la ordenacion para poner el orden de las cabeceras
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pasa la fecha de hoy para crear el enlace a las citas pendientes
        context['desde_fecha'] = datetime.date.today().strftime('%d_%m_%Y')
        # Pasa la ordenacion de la lista de pacientes
        context['head_order'] = self.kwargs['orderby']
        return context

########## ID PACIENTES VIEW ##########

@method_decorator(login_required, name='dispatch')
class id_pacientes_view(ListView):

    model = Paciente
    template_name = 'id_pacientes_tpl.html'

    def get_queryset(self):
        # Se filtra el query para mostrar el idPaciente unico
        qs = super().get_queryset()
        qs = qs.filter(idPaciente = self.kwargs['idPaciente'])
        return qs

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # Obtiene la edad a partir de la fecha de nacimiento
        for paciente in (context['paciente_list']):
            bd = paciente.birthdate

        # Calcula la diferencia entre bd y el dia de hoy
        age = self.calculate_age(bd)
        context['age'] = age

        # Prepara en el contexto la fecha actual para pasarla como DESDE_FECHA
        context['desde_fecha'] = datetime.date.today().strftime('%d_%m_%Y')

        return context

    # Funcion que calcula la edad a partir de la fecha de nacimiento
    def calculate_age(self, bd):
        days_in_year = 365.2425
        age = int((datetime.date.today() - bd).days / days_in_year)
        return age

########## SELECT UN PACIENTE PARA EDITAR VIEW ##########

@method_decorator(login_required, name='dispatch')
class edit_pacientes_view(View):

    # POST
    def post(self, request):

        ctx = dict()
        # Rellena el form con el POST y añade al contexto
        form = edit_pacientes_form(request.POST)
        ctx['form'] = form

        # El form SI es validado
        if form.is_valid():

            # Devuelve el id o el DNI
            show_str = dict()

            # Si devuelve un id comprueba que existe y pasa a edicion...
            if form.cleaned_data['idpac'] != '':

                # Filtra ese id convirtiendolo a numero si se puede
                try:
                    inter_id = int(form.cleaned_data['idpac'])
                except ValueError:
                    inter_id = 0
                existe_id = Paciente.objects.filter(idPaciente = inter_id)

                # Si existe...
                if existe_id:
                    show_str['idPaciente'] = int(form.cleaned_data['idpac'])
                    return HttpResponseRedirect(reverse('edit-id-pacientes', kwargs = show_str))

                # Si no existe pasa a seleccion general
                else:

                    messages.warning(request, 'No existe esa ID. Use la búsqueda ampliada.')
                    return HttpResponseRedirect(reverse('select-pacientes'))

            # Si devuevle un DNI, recupera el registro y lee el id para pasarlo...
            elif form.cleaned_data['dni'] != '':

                # Filtra ese DNI
                existe_dni = Paciente.objects.filter(dni__iexact = form.cleaned_data['dni'])

                # Si existe...
                if existe_dni:
                    inter_paciente = Paciente.objects.get(dni__iexact = form.cleaned_data['dni'])
                    show_str['idPaciente'] = inter_paciente.idPaciente
                    return HttpResponseRedirect(reverse('edit-id-pacientes', kwargs = show_str))

                # Si no existe pasa a seleccion general
                else:

                    messages.warning(request, 'No existe ese DNI. Use la búsqueda ampliada.')
                    return HttpResponseRedirect(reverse('select-pacientes'))

            # Si no marca nada manda a la ventana select general
            else:

                return HttpResponseRedirect(reverse('select-pacientes'))

        # El form NO es validado
        else:

            # Limpia el form y añade al contexto
            form = edit_pacientes_form()
            ctx['form'] = form

            # Mensaje de error en contexto
            ctx['select_pacientes_error'] = 'El formulario contiene errores'

            return render(request, 'edit_pacientes_tpl.html', ctx)

    # GET
    def get(self, request):        
        ctx = dict()
        # Limpia el form y lo añade al contexto
        form = edit_pacientes_form()
        ctx['form'] = form
        return render(request, 'edit_pacientes_tpl.html', ctx)

########## ID para EDIT PACIENTES VIEW ##########

@method_decorator(login_required, name='dispatch')
class edit_id_pacientes_view(UpdateView):

    model = Paciente
    context_object_name = 'paciente'
    pk_url_kwarg = 'idPaciente'
    template_name = 'edit_id_pacientes_tpl.html'
    form_class = edit_id_pacientes_form

    # Arregla el contexto y pasa idPaciente al template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Coge el registro de ese paciente
        context["idPaciente"] = self.kwargs['idPaciente']
        return context

    # Actualiza el campo modifiedby y la foto
    def form_valid(self, form):

        # Sobre la form en bruto se determina si se ha cambiado la foto
        picture_changed = False
        if 'picturefile' in form.changed_data:
            picture_changed = True

        # Pone los registros de control que faltan en una instancia "manejable": paciente
        # Commit = False: evita que se guarde ya en la base de datos
        paciente = form.save(commit = False)

        # Los campos firstupdated y lastupdated se añaden solos

        # Se pone modifiedby
        if str(self.request.user) != 'AmonymousUser':
            paciente.modifiedby = str(self.request.user)
        else:
            paciente.modifiedby = 'unix:' + str(self.request.META['USERNAME'])

        # Limpia y guarda el registro
        paciente.save()

        # Si se actualiza la foto se renombra an DNI y se borra la antigua
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
