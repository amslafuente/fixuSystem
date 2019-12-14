from django.conf.urls import url
from django.urls import path
from gestion_citas import views

urlpatterns = [

    # URLS de gestion_citas

    ########## PRESENTACION DE CITAS ##########

    # Hoy o un dia concreto, en lista o en rejilla
    # Por defecto se ofrece HOY, y de ahí se puede avanzar o retrodecer la fecha a mostrar
    path('hoy/', views.citas_hoy_view.as_view(), name = "citas-hoy"),
    # Modo lista
    path('dia/l/<int:idPaciente>/<str:date>/', views.citas_dia_view.as_view(), name = "citas-dia"),
    # Modo rejilla
    path('dia/r/<int:idPaciente>/<str:date>/', views.citas_dia_grid_view.as_view(), name = "citas-dia-grid"),

    # Vista semanal y mensual de las citas
    path('semanal/<int:year>/<int:week>/', views.citas_semana_view.as_view(), name = "citas-semana"),
    path('mensual/<int:year>/<int:month>/', views.citas_mes_view.as_view(), name = "citas-mes"),

    ########## PRESENTACION DE CITAS DESDE LA APP DE PACIENTES ##########

    # Todas las citas del paciente
    path('paciente/t/<int:idPaciente>/', views.citas_paciente_todas_view.as_view(), name = "citas-paciente-todas"),
    # Todas las citas desde una fecha
    path('paciente/d/<int:idPaciente>/<str:date>/', views.citas_paciente_desdefecha_view.as_view(), name = "citas-paciente-desdefecha"),
    # Todas las citas hasta una fecha
    path('paciente/h/<int:idPaciente>/<str:date>/', views.citas_paciente_hastafecha_view.as_view(), name = "citas-paciente-hastafecha"),

    ########## CREACION DE NUEVAS CITAS ##########

    # NO pasa paciente para crear la cita. Pasa solo fecha y hora de cita.
    path('nueva/<str:date>/<str:hour>/', views.create_citas_view.as_view(), name = "create-citas"),
    # SI pasa paciente para crear la cita. Pasa ademas fecha y hora de cita.
    path('nueva/<int:idPaciente>/<str:date>/<str:hour>/', views.create_citas_paciente_view.as_view(), name = "create-citas-paciente"),

    ########## EDICION DE CITAS Y CAMBIO DE ESTADO ##########
    # Cita concreta
    path('cita/<int:idCita>/', views.id_citas_view.as_view(), name = "id-citas"),
    # Cancela una cita - NO LA BORRA
    path('cancelar/<int:idCita>', views.cancel_citas_view.as_view(), name = "cancel-citas"),
    # Cambia estado de una cita
    path('modificar/<int:idCita>/<str:status>/', views.modif_citas_view.as_view(), name = "modif-citas"),
]
