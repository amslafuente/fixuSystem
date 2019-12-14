########## Views de gestion_citas ##########

from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.http import request, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime
from .models import Cita
from gestion_pacientes.models import Paciente
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from .funct import contexto_dias, app_timegrid
from .forms import create_citas_form, create_citas_paciente_form
from django.contrib import messages

#########################################################
#                                                       #
#       CITAS NO VINCULADAS A UN PACIENTE CONCRETO      #
#                                                       #
#########################################################

########## RELACION COMPLETA DE CITAS PARA HOY ##########

@method_decorator(login_required, name='dispatch')
class citas_hoy_view(ListView):

    model = Cita
    context_object_name = 'citas'
    template_name = 'citas_dia_tpl.html'

    def get_queryset(self):

        # Limita el queryset a las citas de hoy
        current_date = datetime.date.today()
        qs = super().get_queryset()
        qs = Cita.objects.filter(appdate__iexact = current_date).order_by('appdate', 'apptime', 'fk_Consultorio')

        return qs

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # Paciente 0 porque no se pasa paciente a este template
        context['idPaciente'] = 0

        # La fecha de hoy la prepara paaa pasarla al contexto
        current_date = datetime.date.today()
        context['ctx_dias'] = contexto_dias(current_date)

        return context

########## RELACION COMPLETA DE CITAS PARA UN DIA CONCRETO ##########

@method_decorator(login_required, name='dispatch')
class citas_dia_view(ListView):

    model = Cita
    context_object_name = 'citas'
    template_name = 'citas_dia_tpl.html'

    def get_queryset(self, **kwargs):

        # Limita el queryset a las citas del dia pasado en kwargs
        kwarg_date = datetime.datetime.strptime(self.kwargs['date'], '%d_%m_%Y').date()
        qs = super().get_queryset()
        qs = Cita.objects.filter(appdate__iexact = kwarg_date).order_by('appdate', 'apptime', 'fk_Consultorio')

        return qs

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # Paciente 0 porque no se pasa paciente a este template
        context['idPaciente'] = 0

        # La fecha indicada en el GET a traves de kwargs la prepara para pasar al contexto
        kwarg_date = datetime.datetime.strptime(self.kwargs['date'], '%d_%m_%Y').date()
        context['ctx_dias'] = contexto_dias(kwarg_date)

        return context

########## RELACION COMPLETA DE CITAS PARA UN DIA CONCRETO EN FORMATO REJILLA ##########

@method_decorator(login_required, name='dispatch')
class citas_dia_grid_view(ListView):

    model = Cita
    context_object_name = 'citas'
    template_name = 'citas_dia_grid_tpl.html'

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)

        # Query de las citas en la fecha pasada en los kwargs
        kwarg_date = datetime.datetime.strptime(self.kwargs['date'], '%d_%m_%Y').date()

        # Paciente pasado en los kwargs
        kwarg_idpaciente = self.kwargs['idPaciente']

        # SI SE PASA UN idPaciente (idPaciente >0), extrae el paciente concreto y lo pasa al contexto
        if (kwarg_idpaciente > 0):
            qs_paciente = Paciente.objects.get(idPaciente__iexact = kwarg_idpaciente)
            context['paciente'] = qs_paciente
            context['idPaciente'] = qs_paciente.idPaciente
        else:
            context['idPaciente'] = 0

        # Extrae las citas filtradas por fecha
        qs = Cita.objects.filter(appdate__iexact = kwarg_date).order_by('appdate', 'apptime', 'fk_Consultorio')
        # Pasa las citas a un array (cada fila es una tupla con todos los campos de una cita)
        citas = list()
        for cita in qs:
            cita_row = (cita.idCita, cita.fk_Paciente, cita.appdate, cita.apptime, cita.fk_Profesional, cita.fk_Consultorio, cita.status, cita.notes)
            citas.append(cita_row)

        # Contexto que genera las fechas actuales, anteriores y siguentes
        context['ctx_dias'] = contexto_dias(kwarg_date)

        # Contexto con las citas
        context['rejilla'] = app_timegrid(citas, kwarg_date)

        return context

#########################################################
#                                                       #
#        CITAS VINCULADAS A UN PACIENTE CONCRETO        #
#                                                       #
#########################################################

######  CITAS PENDIENTES (FUTURAS) DE UN PACIENTE #######

@method_decorator(login_required, name='dispatch')
class citas_paciente_desdefecha_view(ListView):

    model = Cita
    context_object_name = 'citas'
    template_name = 'citas_paciente_desdefecha_tpl.html'

    # Queryset desde la fecha de hoy, incluida
    def get_queryset(self):
        qs =  super().get_queryset()
        current_date = datetime.date.today()
        kwarg_idpaciente = self.kwargs['idPaciente']
        # Selecciona el paciente pasado en kwargs...
        qs = Cita.objects.filter(fk_Paciente__exact = kwarg_idpaciente)
        # ... y todas sus citas a partir de hoy y futuras
        qs = qs.filter(appdate__gte = current_date).order_by('appdate', 'apptime', 'fk_Consultorio')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Recupera datos del paciente para pasarlos al contexto
        kwarg_idpaciente = self.kwargs['idPaciente']
        qs = Paciente.objects.get(idPaciente__exact = kwarg_idpaciente)
        context['idPaciente'] = kwarg_idpaciente
        context['paciente'] = qs
        # La fecha hasta la que se muestran las citas y pasa al contexto
        # Sirve tb para crear una nueva cita
        context['hasta_fecha'] = datetime.date.today().strftime('%d_%m_%Y')
        context['fecha_cita'] = datetime.date.today().strftime('%d_%m_%Y')
        return context

######  CITAS PASADAS (ANTERIORES) DE UN PACIENTE #######

@method_decorator(login_required, name='dispatch')
class citas_paciente_hastafecha_view(ListView):

    model = Cita
    context_object_name = 'citas'
    template_name = 'citas_paciente_hastafecha_tpl.html'

    # Queryset hasta la fecha de hoy
    def get_queryset(self):
        qs =  super().get_queryset()
        current_date = datetime.date.today()
        # Selecciona el paciente pasado en kwargs...
        qs = Cita.objects.filter(fk_Paciente__exact = self.kwargs['idPaciente'])
        # ... y todas sus citas a partir de hoy y futuras
        qs = qs.filter(appdate__lt = current_date).order_by('appdate', 'apptime', 'fk_Consultorio')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Recupera datos del paciente para pasarlos al contexto
        kwarg_idpaciente = self.kwargs['idPaciente']
        qs = Paciente.objects.get(idPaciente__exact = kwarg_idpaciente)
        context['idPaciente'] = kwarg_idpaciente
        context['paciente'] = qs
        # La fecha hasta la que se muestran las citas y pasa al contexto
        context['desde_fecha'] = datetime.date.today().strftime('%d_%m_%Y')
        context['fecha_cita'] = datetime.date.today().strftime('%d_%m_%Y')
        return context

######  TODAS LAS CITAS PASADAS y FUTURAS DE UN PACIENTE #######

@method_decorator(login_required, name='dispatch')
class citas_paciente_todas_view(ListView):

    model = Cita
    context_object_name = 'citas'
    template_name = 'citas_paciente_todas_tpl.html'

    def get_queryset(self):
        qs =  super().get_queryset()
        qs = Cita.objects.filter(fk_Paciente__exact = self.kwargs['idPaciente']).order_by('appdate', 'apptime', 'fk_Consultorio')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Recupera datos del paciente para pasarlos al contexto
        kwarg_idpaciente = self.kwargs['idPaciente']
        qs = Paciente.objects.get(idPaciente__exact = kwarg_idpaciente)
        context['idPaciente'] = kwarg_idpaciente
        context['paciente'] = qs
        # La fecha desde y hasta la que se muestran las citas y pasa al contexto
        # Sirve tb para crear una nueva cita
        context['desde_fecha'] = datetime.date.today().strftime('%d_%m_%Y')
        context['hasta_fecha'] = datetime.date.today().strftime('%d_%m_%Y')
        context['fecha_cita'] = datetime.date.today().strftime('%d_%m_%Y')
        return context

#########################################################
#                                                       #
#              CREACION Y EDICION DE CITAS              #
#                                                       #
#########################################################

######  PARA CREAR CITAS DESDE EL PACIENTE PASANDO POR EL GRID #######

@method_decorator(login_required, name='dispatch')
class citas_paciente_grid_view____(ListView):

    model = Cita
    context_object_name = 'citas'
    template_name = 'citas_paciente_grid_tpl.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Query de las citas en la fecha pasada el los kwargs
        kwarg_date= datetime.datetime.strptime(self.kwargs['date'], '%d_%m_%Y').date()
        # Selecciona las citas de todos los pacientes
        qs = Cita.objects.filter(appdate__iexact = kwarg_date).order_by('appdate', 'apptime', 'fk_Consultorio')
        # Extrae el paciente concreto para citarlo
        qs2 = Paciente.objects.get(idPaciente__iexact = self.kwargs['idPaciente'])
        # Pasa las citas a un array (cada fila es una tupla con todos los campos de una cita)
        citas = list()
        for cita in qs:
            cita_row = (cita.idCita, cita.fk_Paciente, cita.appdate, cita.apptime, cita.fk_Profesional, cita.fk_Consultorio, cita.status, cita.notes)
            citas.append(cita_row)
        # Contexto que genera las fechas actuales, anteriores y siguentes y la tabla HTML
        context['idPaciente'] = self.kwargs['idPaciente']
        context['Paciente'] = qs2
        context['ctx_dias'] = contexto_dias(kwarg_date)
        context['rejilla'] = app_timegrid(citas, kwarg_date)
        return context

######  CREA CITA DESDE EL GRID, CON FECHA Y HORA PRESELECIONADAS #######

@method_decorator(login_required, name='dispatch')
class create_citas_view(View):

    def post(self, request, date, hour):

        # Inicializa contexto
        ctx = dict()

        # Rellena el form con el POST y la añade  al contexto
        form = create_citas_form(request.POST)
        ctx['form'] = form

        # El form SI es validado
        if form.is_valid():

            # Commit = False: evita que se guarde ya en la base de datos
            cita = form.save(commit = False)

            # Los campos firstupdated y lastupdated se añaden solos

            # Se pone modifiedby
            if str(request.user) != 'AmonymousUser':
                cita.modifiedby = str(request.user)
            else:
                cita.modifiedby = 'unix:' + str(request.META['USERNAME'])

            # Limpia y guarda el registro
            cita.save()

            # Devuelve a las pagina de citas del dia elegido
            ctx = dict()
            ctx['idPaciente'] = 0
            ctx['date'] = date
            return HttpResponseRedirect(reverse('citas-dia', kwargs = ctx))

        # Si no es válido muestra los errores
        else:

            # Mensaje de error en contexto y recarga la pagina
            messages.warning(request, 'El formulario contiene errores')
            return render(request, 'create_citas_tpl.html', ctx)

    def get(self, request, **kwargs):

        # Reinicia contexto y datos iniciales
        ctx = initial_data = dict()

        # Rellena el form con datos de inicio pinchados en el grid y pasados en el URL
        initial_data['appdate'] = datetime.datetime.strptime(self.kwargs['date'], '%d_%m_%Y').date()
        initial_data['apptime'] = datetime.datetime.strptime(self.kwargs['hour'], '%H_%M').time()
        form = create_citas_form(initial = initial_data)
        ctx['form'] = form

        # Va a la pagina de creacion de citas
        return render(request, 'create_citas_tpl.html', ctx)

######  CREA CITA DESDE EL GRID, CON PACIENTE CONCRETO, FECHA Y HORA PRESELECIONADAS #######

@method_decorator(login_required, name='dispatch')
class create_citas_paciente_view(View):

    def post(self, request, idPaciente, date, hour):

        # Inicializa el contexto
        ctx = dict()

        # Rellena el form con el POST y la añade  al contexto
        form = create_citas_paciente_form(request.POST)
        ctx['form'] = form

        # El form SI es validado
        if form.is_valid():

            # Commit = False: evita que se guarde ya en la base de datos
            cita = form.save(commit = False)

            # Los campos firstupdated y lastupdated se añaden solos

            # Se pone el modifiedby
            if str(request.user) != 'AmonymousUser':
                cita.modifiedby = str(request.user)
            else:
                cita.modifiedby = 'unix:' + str(request.META['USERNAME'])

            # Limpia y guarda el registro
            cita.save()

            # Regresa a citas hoy
            return HttpResponseRedirect(reverse('citas-hoy'))

        # Si no es válido muestra los errores
        else:

            # Recupera el paciente pasado en URL
            qs = Paciente.objects.get(idPaciente__iexact = idPaciente)
            # Rellena los datos del contexto necesarios
            ctx['fk_Paciente'] = idPaciente
            ctx['paciente'] = qs
            ctx['date'] = date
            ctx['hour'] = hour
            ctx['ctx_dias'] = contexto_dias(datetime.datetime.strptime(self.kwargs['date'], '%d_%m_%Y').date())

            # Mensaje de error en contexto
            messages.warning(request, 'El formulario contiene errores')

            # Devuelve para corregir
            return render(request, 'create_citas_paciente_tpl.html', ctx)

    def get(self, request, **kwargs):

        # Inicializa el contexto
        ctx = initial_data = dict()

        # Obtiene la info del paciente, la fecha y la hora pasadas en la URL
        kwarg_idpaciente = self.kwargs['idPaciente']
        # Recupera el paciente pasado en URL
        qs = Paciente.objects.get(idPaciente__iexact = kwarg_idpaciente)
        # Fecha y hora
        kwarg_date = datetime.datetime.strptime(self.kwargs['date'], '%d_%m_%Y').date()
        kwarg_time = datetime.datetime.strptime(self.kwargs['hour'], '%H_%M').time()

        # Rellena los datos iniciales del form con los datos pasados en la URL (paciente, fecha y hora)
        initial_data['fk_Paciente'] = kwarg_idpaciente
        initial_data['paciente'] = qs
        initial_data['appdate'] = kwarg_date
        initial_data['apptime'] = kwarg_time

        # Pasa el form con los datos iniciales
        form = create_citas_paciente_form(initial = initial_data)
        ctx['form'] = form

        # Pasa infirmacion de fechas al template
        ctx['ctx_dias'] = contexto_dias(kwarg_date)

        return render(request, 'create_citas_paciente_tpl.html', ctx)

######  CANCELA CITA SIN BORRARLA #######

@method_decorator(login_required, name='dispatch')
class cancel_citas_view(DetailView):

    model = Cita
    context_object_name = 'citas'
    template_name = 'cancel_citas_tpl.html'
    pk_url_kwarg ='idCita'

    def get_context_data(self, **kwargs):

        # Muestra la modificacion para confirmar
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.META.get('HTTP_REFERER', '/')
        return context

    def post(self, request, **kwargs):

        # Determina la cancelación de la cita
        kwarg_next = request.POST['next']
        kwarg_idcita = kwargs['idCita']
        cita = Cita.objects.get(idCita__iexact = kwarg_idcita)
        cita.status = 'Cancelada'
        cita.save()

        # Regresa donde se llamó
        return HttpResponseRedirect(kwarg_next)

######  MODIFICA ESTADO DE UNA CITA #######

class modif_citas_view(DetailView):

    model = Cita
    context_object_name = 'citas'
    template_name = 'modif_citas_tpl.html'
    pk_url_kwarg ='idCita'

    def get_context_data(self, **kwargs):

        # Muestra la modificacion para confirmar
        context = super().get_context_data(**kwargs)
        context['status'] = self.kwargs['status']
        context['next'] = self.request.META.get('HTTP_REFERER', '/')
        return context

    def post(self, request, **kwargs):

        # Determina la modificacion de la cita
        kwarg_next = request.POST['next']
        kwarg_idcita = kwargs['idCita']
        kwarg_status = kwargs['status']
        cita = Cita.objects.get(idCita__iexact = kwarg_idcita)
        cita.status = kwarg_status
        cita.save()

        # Regresa donde se llamó
        return HttpResponseRedirect(kwarg_next)

#####################################################################################

@method_decorator(login_required, name='dispatch')
class citas_semana_view(View):
    pass

@method_decorator(login_required, name='dispatch')
class citas_mes_view(View):
    pass

@method_decorator(login_required, name='dispatch')
class id_citas_view(DetailView):
    pass
