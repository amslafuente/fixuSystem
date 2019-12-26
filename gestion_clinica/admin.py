from django.contrib import admin
from .models import Clinica, Profesional, Consultorio, Proveedor, Equipamiento

# Register your models here.

admin.site.register(Clinica)
admin.site.register(Profesional)
admin.site.register(Consultorio)
admin.site.register(Proveedor)
admin.site.register(Equipamiento)
