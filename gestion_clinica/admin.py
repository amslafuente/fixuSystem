from django.contrib import admin
from .models import Clinica, Profesional, Consultorio

# Register your models here.

admin.site.register(Clinica)
admin.site.register(Profesional)
admin.site.register(Consultorio)
