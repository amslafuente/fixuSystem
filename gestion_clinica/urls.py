from django.urls import path
from gestion_clinica import views



urlpatterns = [

#########################################
#                                       #
#        URLS DE GESTION_CLINICA        #
#                                       #
#########################################

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
    path('error-privilegios/', views.error_privilegios_clinica_view.as_view(), name = 'error-privilegios-clinica'),
    path('error-profesionales/', views.error_profesionales_clinica_view.as_view(), name = 'error-privilegios-profesionales'),
    path('error-root/', views.error_root_clinica_view.as_view(), name = 'error-root'),
    
    ##### Instalaciones y servicios #####

    # Menu Instalaciones y servicios
    path('instalaciones-servicios/', views.instalac_servic_clinica_view.as_view(), name = 'instalac-servic'),
    
    # Consultorios
    path('consultorios/<int:idConsultorio>/', views.id_consultorios_view.as_view(), name = 'id-consultorios'),
    path('consultorios/listado/', views.listado_consultorios_view.as_view(), name = 'listado-consultorios'),
    path('consultorios/nuevo/', views.create_consultorios_view.as_view(), name = 'create-consultorios'),
    path('consultorios/modificar/<int:idConsultorio>/', views.edit_consultorios_view.as_view(), name = 'edit-consultorios'),
    path('consultorios/borrar/<int:idConsultorio>/', views.delete_consultorios_view.as_view(), name = 'delete-consultorios'),
   
     # Equipamiento
    path('equipamiento/<int:idEquipamiento>/', views.id_equipamiento_view.as_view(), name = 'id-equipamiento'),
    path('equipamiento/listado/', views.listado_equipamiento_view.as_view(), name = 'listado-equipamiento'),
    path('equipamiento/nuevo/', views.create_equipamiento_view.as_view(), name = 'create-equipamiento'),
    path('equipamiento/modificar/<int:idEquipamiento>/', views.edit_equipamiento_view.as_view(), name = 'edit-equipamiento'),
    path('equipamiento/borrar/<int:idEquipamiento>/', views.delete_equipamiento_view.as_view(), name = 'delete-equipamiento'),
    
    # Proveedores
    path('proveedores/<int:idProveedor>/', views.id_proveedores_view.as_view(), name = 'id-proveedores'),
    path('proveedores/listado/', views.listado_proveedores_view.as_view(), name = 'listado-proveedores'),
    path('proveedores/nuevo/', views.create_proveedores_view.as_view(), name = 'create-proveedores'),
    path('proveedores/modificar/<int:idProveedor>/', views.edit_proveedores_view.as_view(), name = 'edit-proveedores'),
    path('proveedores/borrar/<int:idProveedor>/', views.delete_proveedores_view.as_view(), name = 'delete-proveedores'),
 
    ##### Profesionales #####

    # Menu profesionales
    path('profesionales/', views.profesionales_clinica_view.as_view(), name = 'profesionales-clinica'),
    
    # Profesionales
    # Seleccion de pacientes a listar
    path('profesionales/consultar/', views.select_profesionales_view.as_view(), name = 'select-profesionales'),
    # Muestra, lista, crea, edita
    path('profesionales/<int:id>/', views.id_profesionales_view.as_view(), name = 'id-profesionales'),
    path('profesionales/listado/<str:fullname>/<str:position>/<str:department>/', views.listado_profesionales_view.as_view(), name = 'listado-profesionales'),
    path('profesionales/nuevo/', views.create_profesionales_view.as_view(), name = 'create-profesionales'),
    path('profesionales/completar/<int:id>/', views.complete_profesionales_view.as_view(), name = 'complete-profesionales'),
    path('profesionales/modificar/<int:id>/', views.edit_profesionales_view.as_view(), name = 'edit-profesionales'),
    # Muestra, lista, crea, edita
    path('profesionales/cambiar-clave/<int:id>/', views.id_clave_profesionales_view.as_view(), name = 'id-clave-profesionales'),
]
