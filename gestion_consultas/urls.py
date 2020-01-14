########## URLs de gestion_consultas ##########

from django.conf.urls import url
from django.urls import path
from gestion_consultas import views

urlpatterns = [

    ##### URLS de gestion_consultas #####

    # Crear una ficha se consulta

    # Previamente seleccionar paciente y cita para creer la ficha
    path('paciente/',views.select_paciente_consultas_view.as_view(), name = 'select-paciente-consultas'),
    path('paciente/citas/',views.select_desdepaciente_consultas_view.as_view(), name = 'select-desdepaciente-consultas'),    
    # Nueva consulta desde cita
    path('nueva/<int:idCita>', views.create_desdecita_consultas_view.as_view(), name = 'create-desdecita-consultas'),
    
    # Seleccion de consultas para ver o editar

    #path('paciente/',views.select_paciente_id_edit_consultas_view.as_view(), name = 'select-paciente-id-edit-consultas'),
    
    # Consulta concreta, consulta a través de cita y consulta a traves de paciente (con fecha o sin fecha)
    path('revisar/<int:idConsulta>/', views.id_consultas_view.as_view(), name = 'id-consultas'),
    path('modificar/<int:idConsulta>/', views.id_consultas_view.as_view(), name = 'edit-consultas'),    

]
