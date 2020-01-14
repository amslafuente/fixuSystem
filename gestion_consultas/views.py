from django.shortcuts import render, reverse
from django.http import request, HttpResponseRedirect
from django.http import request
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime
from .models import Consulta
from gestion_citas.models import Cita
from gestion_pacientes.models import Paciente
from .models import Consulta
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.contrib import messages
from gestion_pacientes.forms import select_pacientes_form

############################################
#                                          #
#     PROCESO DE CREACION DE CONSULTAS     #
#                                          #
############################################

# Busca los pacientes en funcion del dni, apellidos o nomnbre
@method_decorator(login_required, name='dispatch')
class select_paciente_consultas_view(View):   

    # GET
    def get(self, request):

        ctx = dict()
        # Limpia el form y lo añade al contexto
        form = select_pacientes_form()
        ctx['form'] = form
        return render(request, 'select_paciente_consultas_tpl.html', ctx)

    # Se devuelve el form no por POST, sino por GET
    # Ese GET pasa los parametros a select_desdepaciente_consultas_view 

# Lista los pacientes seleccionados con sus citas pendientes, ara eleigir una cita
@method_decorator(login_required, name='dispatch')
class select_desdepaciente_consultas_view(View):


    # GET: Recibe los parametros desde select_paciente_consultas_view
    def get(self, request, **kwargs):
        
        ctx = dict()        
        # Recupera el GET y seleciona los pacientes que cumplen las condiciones
        kwarg_dni = request.GET.get('dni', '')
        kwarg_name = request.GET.get('name', '')        
        kwarg_familyname = request.GET.get('familyname', '')
        kwarg_orderby = request.GET.get('orderby', 'A')
        
        # Todas las citas       
        qs = Cita.objects.select_related('fk_Paciente').all()
        # Ahora elige según en campo con seleccion
        if kwarg_dni != '':
            qs = qs.filter(fk_Paciente__dni__icontains = kwarg_dni)
        if kwarg_name != '':
            qs = qs.filter(fk_Paciente__name__icontains = kwarg_name)
        if kwarg_familyname != '':
            qs = qs.filter(fk_Paciente__familyname__icontains = kwarg_familyname)
        # Ahora excluye las citas pasadas o que ya tienen ficha
        qs = qs.exclude(appdate__lt = datetime.date.today()).exclude(status__icontains = 'Pasa a consulta')
        # Ahora ordena
        if kwarg_orderby == 'N':
            qs = qs.order_by('fk_Paciente__name', 'appdate', 'apptime')
        elif kwarg_orderby == 'D':
            qs = qs.order_by('fk_Paciente__dni', 'appdate', 'apptime')
        elif kwarg_orderby == 'P':
            qs = qs.order_by('fk_Paciente__idPaciente', 'appdate', 'apptime')
        else:
            qs = qs.order_by('fk_Paciente__familyname', 'appdate', 'apptime')
        
        ctx['citas'] = qs
        ctx['head_order'] = kwarg_orderby
              
        return render(request, 'select_desdepaciente_consultas_tpl.html', ctx)


    # POST
    def post(self, request):

        # En el POST se entrega la idCita
        # Con esa idCita se crea la ficha de consulta nueva


        pass

# Crea la ficha de consulta a partir de la cita selecionada
class create_desdecita_consultas_view(View):
    pass

############################################
#                                          #
#          ABRIR/EDITAR CONSULTAS          #
#                                          #
############################################

@method_decorator(login_required, name='dispatch')
class select_paciente_id_edit_consultas_view(View):   
    pass

@method_decorator(login_required, name='dispatch')
class id_consultas_view(DetailView):
    pass


@method_decorator(login_required, name='dispatch')
class edit_consultas_view(UpdateView):
    pass
