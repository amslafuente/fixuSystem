########## URLs de home_pages ##########

from django.urls import path
from .views import home_page_view, menu_pacientes_view,  menu_citas_view, menu_clinica_view
from .views import menu_consultas_view, menu_almacen_view, menu_proveedores_view

urlpatterns = [

    # URLS de home page y menus
    path('', home_page_view.as_view(), name = 'home-page'),
    path('pacientes/', menu_pacientes_view.as_view(), name = 'menu-pacientes'),
    path('citas/', menu_citas_view.as_view(), name = 'menu-citas'),
    path('consultas/', menu_consultas_view.as_view(), name = 'menu-consultas'),
    path('clinica/', menu_clinica_view.as_view(), name = 'menu-clinica'),
    path('almacen/', menu_almacen_view.as_view(), name = 'menu-almacen'),
    path('proveedores/', menu_proveedores_view.as_view(), name = 'menu-proveedores'),
]
