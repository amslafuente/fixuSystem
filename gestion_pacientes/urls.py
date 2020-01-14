from django.urls import path
from gestion_pacientes import views

#########################################
#                                       #
#           URLS DE PACIENTES           #
#                                       #
#########################################

urlpatterns = [

    # Nuevo paciente
    path('nuevo/', views.create_pacientes_view.as_view(), name = 'create-pacientes'),
    # Seleccion de pacientes a listar
    path('seleccionar-listado/', views.select_pacientes_view.as_view(), name = 'select-pacientes'),
    # Listado de pacientes
    path('listado/<str:dni>/<str:name>/<str:familyname>/<str:orderby>/', views.listado_pacientes_view.as_view(), name = 'listado-pacientes'),
    # Mostrar Paciente concreto
    path('id/<int:idPaciente>/', views.id_pacientes_view.as_view(), name = 'id-pacientes'),
    # Seleccion de pacientes a editar
    path('seleccionar-modificar/', views.select_edit_pacientes_view.as_view(), name = 'select-edit-pacientes'),
    # Editar paciente concreto
    path('modificar/<int:idPaciente>/', views.edit_pacientes_view.as_view(), name = 'edit-pacientes'),
]
