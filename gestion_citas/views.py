########## Views de gestion_citas ##########

from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.http import request, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime
from .models import Cita, NotificaCita, ProcesaCita
from gestion_clinica.models import Clinica
from gestion_pacientes.models import Paciente
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views import View
from .funct import contexto_dias, app_timegrid
from .forms import create_citas_form, create_citas_paciente_form, edit_citas_form
from django.contrib import messages
from django.db.models import Q
from fixuSystem.progvars import NOTIFICAR_CON
from django.forms import forms, fields, widgets
from django.forms.widgets import NumberInput
from django.core.mail import send_mail
import locale
import smtplib

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
        ctx = super().get_context_data(**kwargs)
        # Paciente 0 porque no se pasa paciente a este template
        ctx['idPaciente'] = 0
        # La fecha de hoy la prepara para pasarla al contexto
        current_date = datetime.date.today()
        ctx['ctx_dias'] = contexto_dias(current_date)

        return ctx

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
        ctx = super().get_context_data(**kwargs)

        # Paciente 0 porque no se pasa paciente a este template
        ctx['idPaciente'] = 0

        # La fecha indicada en el GET a traves de kwargs la prepara para pasar al contexto
        kwarg_date = datetime.datetime.strptime(self.kwargs['date'], '%d_%m_%Y').date()
        ctx['ctx_dias'] = contexto_dias(kwarg_date)

        return ctx

########## RELACION COMPLETA DE CITAS PARA UN DIA CONCRETO EN FORMATO REJILLA ##########

@method_decorator(login_required, name='dispatch')
class citas_dia_grid_view(ListView):

    model = Cita
    context_object_name = 'citas'
    template_name = 'citas_dia_grid_tpl.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Query de las citas en la fecha pasada en los kwargs
        kwarg_date = datetime.datetime.strptime(self.kwargs['date'], '%d_%m_%Y').date()

        # Paciente pasado en los kwargs
        kwarg_idpaciente = self.kwargs['idPaciente']

        # SI SE PASA UN idPaciente (idPaciente >0), extrae el paciente concreto y lo pasa al contexto
        if (kwarg_idpaciente > 0):
            qs_paciente = Paciente.objects.get(idPaciente__iexact = kwarg_idpaciente)
            ctx['paciente'] = qs_paciente
            ctx['idPaciente'] = qs_paciente.idPaciente
        else:
            ctx['idPaciente'] = 0

        # Extrae las citas filtradas por fecha
        qs = Cita.objects.filter(appdate__iexact = kwarg_date).order_by('appdate', 'apptime', 'fk_Consultorio')
        
        # Pasa las citas a un array (cada fila es una tupla con todos los campos de una cita)
        citas = list()
        for cita in qs:
            cita_row = (cita.idCita, cita.fk_Paciente, cita.appdate, cita.apptime, cita.fk_Profesional, cita.fk_Consultorio, cita.status, cita.notes)
            citas.append(cita_row)
        print(citas)
        # Contexto que genera las fechas actuales, anteriores y siguentes
        ctx['ctx_dias'] = contexto_dias(kwarg_date)

        # Contexto con las citas
        ctx['rejilla'] = app_timegrid(citas, kwarg_date)        

        return ctx

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

    # Queryset de citas del paciente desde la fecha de hoy, incluida
    def get_queryset(self):
        qs =  super().get_queryset()
        current_date = datetime.date.today()
        kwarg_idpaciente = self.kwargs['idPaciente']
        # Selecciona el paciente pasado en kwargs...
        qs = Cita.objects.filter(fk_Paciente__exact = kwarg_idpaciente)
        # ... y todas sus citas a partir de hoy y futuras
        qs = qs.filter(appdate__gte = current_date).order_by('appdate', 'apptime', 'fk_Consultorio')
        
        return qs
    
    # Genera contexto
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Recupera datos del paciente para pasarlos al contexto
        kwarg_idpaciente = self.kwargs['idPaciente']
        qs = Paciente.objects.get(idPaciente__exact = kwarg_idpaciente)
        ctx['idPaciente'] = kwarg_idpaciente
        ctx['paciente'] = qs
        # La fecha hasta la que se muestran las citas y pasa al contexto
        # Sirve tb para crear una nueva cita
        ctx['hasta_fecha'] = datetime.date.today().strftime('%d_%m_%Y')
        ctx['fecha_cita'] = datetime.date.today().strftime('%d_%m_%Y')
        
        return ctx

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
        ctx = super().get_context_data(**kwargs)
        # Recupera datos del paciente para pasarlos al contexto
        kwarg_idpaciente = self.kwargs['idPaciente']
        qs = Paciente.objects.get(idPaciente__exact = kwarg_idpaciente)
        ctx['idPaciente'] = kwarg_idpaciente
        ctx['paciente'] = qs
        # La fecha hasta la que se muestran las citas y pasa al contexto
        ctx['desde_fecha'] = datetime.date.today().strftime('%d_%m_%Y')
        ctx['fecha_cita'] = datetime.date.today().strftime('%d_%m_%Y')
       
        return ctx

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
        ctx = super().get_context_data(**kwargs)
        # Recupera datos del paciente para pasarlos al contexto
        kwarg_idpaciente = self.kwargs['idPaciente']
        qs = Paciente.objects.get(idPaciente__exact = kwarg_idpaciente)
        ctx['idPaciente'] = kwarg_idpaciente
        ctx['paciente'] = qs
        # La fecha desde y hasta la que se muestran las citas y pasa al contexto
        # Sirve tb para crear una nueva cita
        ctx['desde_fecha'] = datetime.date.today().strftime('%d_%m_%Y')
        ctx['hasta_fecha'] = datetime.date.today().strftime('%d_%m_%Y')
        ctx['fecha_cita'] = datetime.date.today().strftime('%d_%m_%Y')
        
        return ctx

#########################################################
#                                                       #
#              CREACION Y EDICION DE CITAS              #
#                                                       #
#########################################################

@method_decorator(login_required, name='dispatch')
class id_citas_view(DetailView):
    pass

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
            
            # Devuelve a las pagina de citas del dia elegido
            ctx = dict()
            ctx['idPaciente'] = idPaciente
            ctx['date'] = date
            
            return HttpResponseRedirect(reverse('citas-dia', kwargs = ctx))

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


######  EDIT THE NOTES OF AN APPOINTMENT #######
######  Any other change: cancel and create a new one ######

@method_decorator(login_required, name='dispatch')
class edit_citas_view(View):
    
    def post(self, request, **kwargs):

        # Inicializa el contexto
        ctx = dict()

        # Rellena el form con el POST y la añade  al contexto
        form = edit_citas_form(request.POST)
        ctx['form'] = form

        # El form SI es validado
        if form.is_valid():

            # Obtiene la info de la cita concreta
            kwarg_idcita = self.kwargs['idCita'] 
             # Recupera la cita pasada en URL
            qs = Cita.objects.get(idCita__iexact = kwarg_idcita)
            # Almacena las nuevas notas y guarda
            qs.notes = form.cleaned_data['notes']
            qs.save()
            
            # Regresa donde se llamó
            kwarg_next = request.POST['next']
            return HttpResponseRedirect(kwarg_next)

        # Si el form NO es validado
        else:

            messages.warning(request, 'Error en el formulario.')

            # Regresa al META Referer
            return render(request, 'edit_citas_tpl.html', ctx)

    def get(self, request, **kwargs):

        # Inicializa el contexto
        ctx = initial_data = dict()

        # Obtiene la info de la cita concreta
        kwarg_idcita = self.kwargs['idCita']
        # Recupera la cita pasada en URL
        qs = Cita.objects.get(idCita__iexact = kwarg_idcita)
    
        # Rellena los datos iniciales del form con los datos pasados en la URL (cita)
        initial_data['notes'] = qs.notes

        # Pasa el form con los datos iniciales
        form = edit_citas_form(initial = initial_data)
        ctx['form'] = form
        ctx['citas'] = qs

        # Determina la pagina de procedencia del click
        ctx['next'] = self.request.META.get('HTTP_REFERER', '/')

        # Determina si la cita ya ha pasado (no tiene sentido modificarla)
        kwarg_idcita = self.kwargs['idCita']
        kwarg_today = datetime.date.today()
        cita = Cita.objects.get(idCita__iexact = kwarg_idcita)
        if cita.appdate < kwarg_today:
            ctx['old_app'] = True

        return render(request, 'edit_citas_tpl.html', ctx)

######  CANCELA CITA SIN BORRARLA #######

@method_decorator(login_required, name='dispatch')
class cancel_citas_view(DetailView):

    model = Cita
    context_object_name = 'citas'
    template_name = 'cancel_citas_tpl.html'
    pk_url_kwarg ='idCita'

    def get_context_data(self, **kwargs):
        # Determina la pagina de procedencia del click
        ctx = super().get_context_data(**kwargs)
        ctx['next'] = self.request.META.get('HTTP_REFERER', '/')

        # Determina si la cita ya ha pasado (no tiene sentido cancelarla)
        kwarg_idcita = self.kwargs['idCita']
        kwarg_today = datetime.date.today()
        cita = Cita.objects.get(idCita__iexact = kwarg_idcita)
        if cita.appdate < kwarg_today:
            ctx['old_app'] = True
        
        return ctx

    # Determina la cancelación de la cita
    def post(self, request, **kwargs):       
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

    # Muestra la modificacion para confirmar
    def get_context_data(self, **kwargs):        
        ctx = super().get_context_data(**kwargs)
        ctx['status'] = self.kwargs['status']
        ctx['next'] = self.request.META.get('HTTP_REFERER', '/')

        # Determina si la cita ya ha pasado (no tiene sentido modificarla)
        kwarg_idcita = self.kwargs['idCita']
        kwarg_today = datetime.date.today()
        cita = Cita.objects.get(idCita__iexact = kwarg_idcita)
        if cita.appdate < kwarg_today:
            ctx['old_app'] = True

        return ctx

    # Completa la modificacion de la cita
    def post(self, request, **kwargs):        
        kwarg_idcita = kwargs['idCita']
        kwarg_status = kwargs['status']
        kwarg_next = request.POST['next']
        cita = Cita.objects.get(idCita__iexact = kwarg_idcita)
        cita.status = kwarg_status
        cita.save()

        # Regresa donde se llamó
        return HttpResponseRedirect(kwarg_next)

######  PROCESAR CITAS #######

@method_decorator(login_required, name='dispatch')
class procesar_citas_view(View):

    def get(self, request):

        ctx = dict()

        notif = NotificaCita.objects.last()
        proc = ProcesaCita.objects.last()
        try:
            ctx['last_notif'] = notif.notifLastrun
            ctx['with_errors'] = notif.witherrors
        except:
            ctx['last_notif'] = 'Sin fecha'
        try:
            ctx['last_proc'] = proc.procLastrun
        except:
            ctx['last_proc'] = 'Sin fecha'

        ctx['day'] = NOTIFICAR_CON
        ctx['untilday'] = 0

        return render(request, 'procesar_citas_tpl.html', ctx)

@method_decorator(login_required, name='dispatch')
class recordatorios_citas_view(View):

    def post(self, request):
        
        # Comprueba si es superuser
        if not request.user.is_superuser:

            return HttpResponseRedirect(reverse('procesar-citas'))

        # Inicializa contexto
        ctx = dict()

        # Rellena el form con el POST y la añade  al contexto
        form = customNotifDias(request.POST)        
        ctx['form'] = form

        # SI los datos son válidos
        if form.is_valid:

            kwarg_day = int(request.POST['day'])
            try:
                kwarg_untilday = request.POST['untilday']
            except:
                kwarg_untilday = False
            kwarg_date = datetime.date.today()
            kwarg_notifydate = kwarg_date + datetime.timedelta(days = kwarg_day)
            
            ctx['notifydate'] = kwarg_notifydate
           
            if kwarg_untilday:
                
                ctx['untilday'] = 'y anteriores'

            # Queries
            # Si no selecciona interdays
            if not kwarg_untilday:
                emailcount = Cita.objects.filter(appdate = kwarg_notifydate).select_related('fk_Paciente').filter(fk_Paciente__notifyappoint = True).filter(fk_Paciente__notifyvia__iexact = 'email').count()
                qsemail = Cita.objects.filter(appdate = kwarg_notifydate).select_related('fk_Paciente').filter(fk_Paciente__notifyappoint = True).filter(fk_Paciente__notifyvia__iexact = 'email')
                qstelef = Cita.objects.filter(appdate = kwarg_notifydate).select_related('fk_Paciente').filter(fk_Paciente__notifyappoint = True).exclude(fk_Paciente__notifyvia__iexact = 'email')
            # Si selecciona interdays
            else:
                emailcount = Cita.objects.filter(appdate__gt = kwarg_date, appdate__lte = kwarg_notifydate).select_related('fk_Paciente').filter(fk_Paciente__notifyappoint = True).filter(fk_Paciente__notifyvia__iexact = 'email').count() 
                qsemail = Cita.objects.filter(appdate__gt = kwarg_date, appdate__lte = kwarg_notifydate).select_related('fk_Paciente').filter(fk_Paciente__notifyappoint = True).filter(fk_Paciente__notifyvia__iexact = 'email')
                qstelef = Cita.objects.filter(appdate__gt = kwarg_date, appdate__lte = kwarg_notifydate).select_related('fk_Paciente').filter(fk_Paciente__notifyappoint = True).exclude(fk_Paciente__notifyvia__iexact = 'email')
           
            ctx['emailcount'] = emailcount
            
            ##### Notifica por email #####

            # Recupera datos de la clinica (from)
            clinica = Clinica.objects.first()
            # Recupera campos de las citas
            qsemail = qsemail.values('fk_Paciente__familyname', 'fk_Paciente__name', 'fk_Paciente__email', 'fk_Paciente__phone1', 'fk_Paciente__phone2', 'appdate', 'apptime')

            # Construye tupla de cada mensaje
            # asunto, mensaje, from, to
            locale.setlocale(locale.LC_ALL,'es_ES')
            
            lista_emails = list()          
            for email in qsemail:
                asunto = 'Recordatorio de cita'                
                apellidos = email['fk_Paciente__familyname']
                nombre = email['fk_Paciente__name']
                fechacita = email['appdate']
                horacita = email['apptime']
                mensaje = 'Estimado/a Sr./Sra. ' + apellidos + ':\r\n\n'
                mensaje = mensaje + 'Le recordamos que tiene una cita pendiente en ' + clinica.clinicname + ' '
                mensaje = mensaje + 'el ' + datetime.date.strftime(fechacita, '%A, %d de %B de %Y') + ', a las ' + datetime.time.strftime(horacita, '%H:%M')  + ' horas.\r\n\n'
                mensaje = mensaje + '---\r\n'
                mensaje = mensaje + '  ' + clinica.clinicname + '\r\n'
                mensaje = mensaje + '  ' + clinica.fulladdress + '\r\n'
                mensaje = mensaje + '  Teléfono : ' + str(clinica.phone1) + '\r\n'
                mensaje = mensaje + '  Email : ' + clinica.email + '\r\n'                
                email_from = clinica.email
                email_to = email['fk_Paciente__email']                
                telef1 = email['fk_Paciente__phone1']
                telef2 = email['fk_Paciente__phone2']                
                lista_emails.append((asunto, mensaje, email_from, email_to, apellidos, nombre, telef1, telef2, fechacita, horacita))

            locale.resetlocale(category=locale.LC_ALL)
            
            # Gestiona el envio de los email
            emails_enviados = 0
            emails_noenviados = 0
            emails_errores = list()
            emails_to_phone = list()

            for i in range(0, len(lista_emails)):
                try:
                    asunto = lista_emails[i][0]
                    mensaje = lista_emails[i][1]
                    correo_de = lista_emails[i][2]
                    correo_para = list()
                    correo_para.append(lista_emails[i][3])
                    emails_enviados = emails_enviados + send_mail(asunto, mensaje, correo_de, correo_para, fail_silently = False)
                # Si falla en el envío guarda el mensaje para notificar por telefono
                except Exception as e:
                    emails_noenviados += 1
                    emails_errores.append((correo_para, e))
                    apellidos = lista_emails[i][4]
                    nombre = lista_emails[i][5]
                    telef1 = lista_emails[i][6]
                    telef2 = lista_emails[i][7]
                    fechacita = lista_emails[i][8]
                    horacita = lista_emails[i][9]
                    emails_to_phone.append((apellidos, nombre, telef1, telef2, fechacita, horacita))

            ctx['emailsent'] = emails_enviados
            ctx['emailunsent'] = emails_noenviados
            ctx['emailerrors'] = emails_errores
            ctx['emails2phone'] = emails_to_phone

            ##### Notifica por telefono #####           

            # Lista de notificacion por telefono
            restelef = list()
            qstelef = qstelef.values('fk_Paciente__familyname', 'fk_Paciente__name', 'fk_Paciente__phone1', 'fk_Paciente__phone2', 'appdate', 'apptime')
            for telef in qstelef:
                apellidos = telef['fk_Paciente__familyname']
                nombre = telef['fk_Paciente__name']
                telef1 = telef['fk_Paciente__phone1']
                telef2 = telef['fk_Paciente__phone2']                
                fechacita = telef['appdate']
                horacita = telef['apptime']
                restelef.append((apellidos, nombre, telef1, telef2, fechacita, horacita))

            ctx['restelef'] = restelef

            ##### Coloca el registro que indica la ultima fecha de actualización #####
            qsnotif = NotificaCita()
            # Si ha habido errores en el envio de email lo indica
            if emails_noenviados > 0:
                qsnotif.witherrors = True
            else:
                qsnotif.witherrors = False
            # Se pone modifiedby
            if str(request.user) != 'AmonymousUser':
                qsnotif.modifiedby = str(request.user)
            else:
                qsnotif.modifiedby = 'unix:' + str(request.META['USERNAME'])
            qsnotif.save()

            return render(request, 'recordatorios_result_citas_tpl.html', ctx)

        # Si no son validos
        else:

            messages.warning(request, 'Error en el formulario.')

            return render(request, 'recordatorios_citas_tpl.html', ctx)

    def get(self, request):

        ctx = dict()

        # Dias de antelacion pasados en el GET o por defecto
        kwarg_day = int(request.GET.get('day', default = NOTIFICAR_CON))
        kwarg_untilday = request.GET.get('untilday', default = False)
        if kwarg_untilday == 'on':
            kwarg_untilday = True
        else:
            kwarg_untilday = False

        # Pasa la form con dias a modificar
        form = customNotifDias(initial={'day': kwarg_day, 'untilday': kwarg_untilday})
        ctx['form'] = form

        # Cuenta los registros que cumplen las condiciones de ser notificados por email o telefono
        kwarg_date = datetime.date.today()
        kwarg_notifydate = kwarg_date + datetime.timedelta(days = kwarg_day)
   
        # Si se señala UNTILDAYS, se incluye en la busqueda el rango de fechas
        # Si no se indica UNTILDAYS solo se usca una fecha concreta
        if not kwarg_untilday:
            numregsemail = Cita.objects.filter(appdate = kwarg_notifydate).select_related('fk_Paciente').filter(fk_Paciente__notifyappoint = True).filter(fk_Paciente__notifyvia__iexact = 'email').count()
            numregstelef = Cita.objects.filter(appdate = kwarg_notifydate).select_related('fk_Paciente').filter(fk_Paciente__notifyappoint = True).exclude(fk_Paciente__notifyvia__iexact = 'email').count()
        else:
            numregsemail = Cita.objects.filter(appdate__gt = kwarg_date, appdate__lte = kwarg_notifydate).select_related('fk_Paciente').filter(fk_Paciente__notifyappoint = True).filter(fk_Paciente__notifyvia__iexact = 'email').count()
            numregstelef = Cita.objects.filter(appdate__gt = kwarg_date, appdate__lte = kwarg_notifydate).select_related('fk_Paciente').filter(fk_Paciente__notifyappoint = True).exclude(fk_Paciente__notifyvia__iexact = 'email').count()
        
        # Muestra lo que hay a notificar 
        ctx['numregsemail'] = numregsemail
        ctx['numregstelef'] = numregstelef
        
        return render(request, 'recordatorios_citas_tpl.html', ctx)

class customNotifDias(forms.Form):
    
    day = fields.IntegerField(required = False)
    untilday = fields.BooleanField(required = False)
    day.widget = widgets.NumberInput(attrs={'style': 'width: 50px', 'min': 0, 'max': 99})   
  
@method_decorator(login_required, name='dispatch')
class pasadas_canceladas_citas_view(View):

    def post(self, request):
        
         # Comprueba si es superuser
        if not request.user.is_superuser:

            return HttpResponseRedirect(reverse('procesar-citas'))

        # Si es superuser continua
        ctx = dict()

        # Query
        queryexclude = Q(status__iexact = 'Pasa a consulta')
        querydelete = (Q(appdate__lt = datetime.date.today()) | Q(status__iexact = 'Cancelada'))
        try:
            qscita = Cita.objects.exclude(queryexclude).filter(querydelete).count()
            numregs = 0
            qsproc = ProcesaCita()
            # Se pone modifiedby
            if str(request.user) != 'AmonymousUser':
                qsproc.modifiedby = str(request.user)
            else:
                qsproc.modifiedby = 'unix:' + str(request.META['USERNAME'])
            qsproc.save()
        except:
            numregs = Cita.objects.exclude(queryexclude).filter(querydelete).count()

        if numregs > 0:
            ctx['mensaje'] = 'Error al procesar la base de datos.'
            ctx['numregs'] = numregs
        else:
            ctx['mensaje'] = 'No hay citas más para procesar.'            

        return render(request, 'pasadas_canceladas_citas_tpl.html', ctx)

    def get(self, request):
        
        ctx = dict()
        
        # Comprueba si es superuser
        if not request.user.is_superuser:

            return HttpResponseRedirect(reverse('procesar-citas'))
     
        # Cuenta los registros que cumplen las condiciones de ser pasada, canceladas y sin consulta
        queryexclude = Q(status__iexact = 'Pasa a consulta')
        querydelete = (Q(appdate__lt = datetime.date.today()) | Q(status__iexact = 'Cancelada'))
        
        try:
            numregs = Cita.objects.exclude(queryexclude).filter(querydelete).count()
        except:
            numregs = 0
        
        if numregs > 0:
            ctx['mensaje'] = 'Se va a proceder a BORRAR de la base de datos las citas ya pasadas, o canceladas, que no han generado ninguna ficha de consulta.'
            ctx['numregs'] = numregs
        else:
            ctx['mensaje'] = 'No hay citas para procesar.'            

        return render(request, 'pasadas_canceladas_citas_tpl.html', ctx)

#####################################################################################

@method_decorator(login_required, name='dispatch')
class citas_semana_view(View):
    pass

@method_decorator(login_required, name='dispatch')
class citas_mes_view(View):
    pass


