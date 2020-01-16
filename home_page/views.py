from django.views.generic import TemplateView



#########################################
#                                       #
#              MENU PRINCIPAL           #
#                                       #
#########################################

class home_page_view(TemplateView):
    template_name = "home_page_tpl.html"

class menu_pacientes_view(TemplateView):
    template_name = "menu_pacientes_tpl.html"

class menu_citas_view(TemplateView):
    template_name = "menu_citas_tpl.html"

class menu_consultas_view(TemplateView):
    template_name = "menu_consultas_tpl.html"

class menu_clinica_view(TemplateView):
    template_name = "menu_clinica_tpl.html"
