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
from .forms import select_paciente_consultas_form


##### PROCESO DE CREACION DE CONSULTAS #####

# Busca los pacientes en funcion del dni, apellidos o nomnbre
@method_decorator(login_required, name='dispatch')
class select_paciente_consultas_view(View):   

    # GET
    def get(self, request):

        ctx = dict()
        # Limpia el form y lo añade al contexto
        form = select_paciente_consultas_form()
        ctx['form'] = form
        return render(request, 'select_paciente_consultas_tpl.html', ctx)

# Lista los pacientes seleccionados con sus citas pendientes, ara eleigir una cita
@method_decorator(login_required, name='dispatch')
class select_desdepaciente_consultas_view(View):

    # POST
    def post(self, request):

        # En el POST se entrega la idCita
        # Con esa idCita se crea la ficha de consulta nueva


        pass

    # GET
    def get(self, request, **kwargs):
        
        ctx = dict()
        
        # Seleciona los pacientes que cumplen las condiciones
        kwarg_dni = request.GET.get('dni', '')
        kwarg_name = request.GET.get('name', '')        
        kwarg_familyname = request.GET.get('familyname', '')
        kwarg_orderby = request.GET.get('orderby', 'A')

        pacientes = Paciente.objects.all()
        if kwarg_dni != '':
            pacientes = pacientes.filter(dni__icontains = kwarg_dni)
        if kwarg_name != '':
            pacientes = pacientes.filter(name__icontains = kwarg_name)
        if kwarg_familyname != '':
            pacientes = pacientes.filter(familyname__icontains = kwarg_familyname)
        if kwarg_orderby == 'N':
            pacientes = pacientes.order_by('name')
        elif kwarg_orderby == 'D':
            pacientes = pacientes.order_by('dni')
        else:
            pacientes = pacientes.order_by('familyname')

        # Para cada paciente seleccionado busca sus citas PENDIENTES, no pasadas
        listacitas = list()
        for paciente in pacientes:
            citas = Cita.objects.filter(fk_Paciente__idPaciente = paciente.idPaciente).exclude(appdate__lt = datetime.date.today()).exclude(status__icontains = 'Pasa a consulta')
            for cita in citas:
                citaspaciente = (paciente.idPaciente, paciente.familyname, paciente.name, cita.idCita, cita.appdate)
                listacitas.append(citaspaciente)                
        ctx['listacitas'] = listacitas
            
        return render(request, 'select_desdepaciente_consultas_tpl.html', ctx)

# Crea la ficha de consulta a partir de la cita selecionada
class create_desdecita_consultas_view(View):
    pass

##### ID DE CONSULTA #####


class id_consultas_view(DetailView):
    pass


##### EDICION  DE CONSULTAS #####


class edit_consultas_view(UpdateView):
    pass
