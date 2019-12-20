

from django.urls import path
from gestion_clinica import views

urlpatterns = [

    ##### URLS de gestion_clinica #####

    ##### Clinica #####

    # ID CLINICA: Muestra los datos de la clínica
    path('info-clinica/', views.info_clinica_view.as_view(), name = 'info-clinica'),
    # Inicia los datos de la clínica
    path('iniciar/', views.init_clinica_view.as_view(), name = 'init-clinica'),
    # Edita los datos de la clínica
    path('modificar/<int:idClinica>/', views.edit_info_clinica_view.as_view(), name = 'edit-info-clinica'),
    # Error si trata de crear mas de una clinica
    path('error-iniciar/', views.error_init_clinica_view.as_view(), name = 'error-init-clinica'),
    # Error si trata de un usuario NO SUPERUSER
    path('error-usuario/', views.error_init_usuario_view.as_view(), name = 'error-init-usuario'),

    ##### Instalaciones y servicios #####

    # Instalaciones y servicios
    path('instalaciones-servicios/', views.instalac_servic_clinica_view.as_view(), name = 'instalac-servic'),
    
    # Consultorios
    path('consultorios/<int:idConsultorio>/', views.id_consultorios_view.as_view(), name = 'id-consultorios'),
    path('consultorios/listado/', views.listado_consultorios_view.as_view(), name = 'listado-consultorios'),
    path('consultorios/nuevo/', views.create_consultorios_view.as_view(), name = 'create-consultorios'),
    path('consultorios/modificar/<int:idConsultorio>/', views.edit_consultorios_view.as_view(), name = 'edit-consultorios'),
    path('consultorios/borrar/<int:idConsultorio>/', views.delete_consultorios_view.as_view(), name = 'delete-consultorios'),
    # Error si trata de un usuario NO STAFF
    path('consultorios/error-usuario/', views.error_consultorios_usuario_view.as_view(), name = 'error-consultorios-usuario'),

     # Equipamiento
    path('equipamiento/<int:idEquipamiento>/', views.id_equipamiento_view.as_view(), name = 'id-equipamiento'),
    path('equipamiento/listado/', views.listado_equipamiento_view.as_view(), name = 'listado-equipamiento'),
    path('equipamiento/nuevo/', views.create_equipamiento_view.as_view(), name = 'create-equipamiento'),
    path('equipamiento/modificar/<int:idEquipamiento>/', views.edit_equipamiento_view.as_view(), name = 'edit-equipamiento'),
    path('equipamiento/borrar/<int:idEquipamiento>/', views.delete_equipamiento_view.as_view(), name = 'delete-equipamiento'),
    # Error si trata de un usuario NO STAFF
    path('equipamiento/error-usuario/', views.error_equipamiento_usuario_view.as_view(), name = 'error-equipamiento-usuario'),





    ##### Profesionales #####

    # Profesionales
    path('profesionales/', views.profesionales_clinica_view.as_view(), name = 'profesionales'),




]
