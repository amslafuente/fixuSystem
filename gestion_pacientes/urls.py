########## URLs de gestion_pacientes ##########

from django.urls import path
from gestion_pacientes import views

urlpatterns = [

    ##### URLS de gestion_pacientes #####

    # Nuevo paciente y confirmacion de nuevo paciente
    path('nuevo/', views.create_pacientes_view.as_view(), name = 'create-pacientes'),
    path('nuevo_confirma/', views.create_pacientes_confirm_view.as_view(), name = 'create-pacientes-confirm'),

    # Seleccion de pacientes a listar
    path('consultar/', views.select_pacientes_view.as_view(), name = 'select-pacientes'),
    # Listado de pacientes
    path('mostrar/<str:dni>/<str:name>/<str:familyname>/<str:orderby>/', views.show_pacientes_view.as_view(), name = 'show-pacientes'),
    # Mostrar Paciente concreto
    path('mostrar/<int:idPaciente>/', views.id_pacientes_view.as_view(), name = 'id-pacientes'),

    # Seleccion de pacientes a editar
    path('editar/', views.edit_pacientes_view.as_view(), name = 'edit-pacientes'),
    # Editar paciente concreto
    path('editar/<int:idPaciente>/', views.edit_id_pacientes_view.as_view(), name = 'edit-id-pacientes'),

]
