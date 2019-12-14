########## Views de gestion_consultas ###########

from django.shortcuts import render, reverse
from django.http import request
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime
from .models import Consulta
from gestion_citas.models import Cita
from gestion_pacientes.models import Paciente
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.contrib import messages
from .forms import create_consultas_form


class create_consultas_view(View):


    def get(self, request):

        # Inicializa contexto
        ctx = dict()

        # Pasa una form vacia
        form = create_consultas_form()
        ctx['form'] = form

        return render(request, 'create_consultas_tpl.html', ctx)


class create_consultas_citas_view(View):

    pass



class id_consultas_view(DetailView):

    pass

class id_consultas_citas_view(DetailView):

    pass

class id_consultas_pacientes_view(DetailView):

    pass
