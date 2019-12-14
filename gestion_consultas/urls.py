########## URLs de gestion_consultas ##########

from django.conf.urls import url
from django.urls import path
from gestion_consultas import views

urlpatterns = [

    ##### URLS de gestion_consultas #####

    # Nueva consulta
    path('nueva/', views.create_consultas_view.as_view(), name = 'create-consultas'),
    # Nueva consulta desde cita
    path('nueva/<int:idCita>', views.create_consultas_citas_view.as_view(), name = 'create-consultas-citas'),

    # Seleccion de consultas
    # Consulta concreta, consulta a través de cita y consulta a traves de paciente (con fecha o sin fecha)
    path('consulta/<int:idConsulta>/', views.id_consultas_view.as_view(), name = 'id-consultas'),
    path('consulta/cita/<int:idCita>/', views.id_consultas_citas_view.as_view(), name = '"id-consultas-citas'),
    path('consulta/<int:idPaciente/', views.id_consultas_pacientes_view.as_view(), name = '"id-consultas-pacientes'),
]
