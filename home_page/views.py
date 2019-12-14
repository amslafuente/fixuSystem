########## VIEW DE HOME PAGE ##########

from django.views.generic import TemplateView

########## Home page ##########

# View para crear la home page
# Usa el template home_page_tpl

class home_page_view(TemplateView):

    template_name = "home_page_tpl.html"

########## Menu de pacientes ##########

# View para crear el menú de pacientes
# Usa el template menu_pacientes_tpl

class menu_pacientes_view(TemplateView):

    template_name = "menu_pacientes_tpl.html"

class menu_citas_view(TemplateView):

    template_name = "menu_citas_tpl.html"

class menu_consultas_view(TemplateView):

    template_name = "menu_consultas_tpl.html"

class menu_clinica_view(TemplateView):

    template_name = "menu_clinica_tpl.html"

class menu_almacen_view(TemplateView):
    pass

class menu_proveedores_view(TemplateView):
    pass
