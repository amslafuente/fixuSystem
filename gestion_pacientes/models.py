from django.db import models
from django.urls import reverse
from django.db.models.fields.related import ForeignKey
from fixuSystem.progvars import modeVia, sexDef

########## TABLA DE GESTION DE PACIENTES ##########

class Paciente(models.Model):

    idPaciente = models.AutoField(primary_key = True, unique = True)
    dni = models.CharField("DNI", max_length = 9, db_index = True, unique = True)
    name = models.CharField("Nombre", max_length = 50)
    familyname = models.CharField("Apellidos", max_length = 100)
    birthdate = models.DateField("Fecha de nacimiento", help_text="DD/MM/AAAA")
    sex = models.CharField("Sexo", max_length = 50, choices = sexDef, default = 'No declarado')
    address = models.CharField("Dirección", max_length = 250)
    postcode = models.PositiveIntegerField("C. Postal")
    city = models.CharField("Ciudad", max_length = 50)
    province = models.CharField("Provincia", max_length = 50,  null = True, blank = True)
    country = models.CharField("País", max_length = 60,  null = True, blank = True, default = 'España')
    email = models.EmailField("Correo electrónico", max_length = 75, blank = True, null = True)
    phone1 = models.PositiveIntegerField("Teléfono principal")
    phone2 = models.PositiveIntegerField("Teléfono alternativo", null = True, blank = True)
    job = models.CharField("Ocupación", max_length = 20, blank = True)
    notes = models.TextField("Notas", blank = True)
    picturefile = models.ImageField("Archivo foto", upload_to = 'pacientes/',  null = True, blank = True)
    notifyappoint = models.BooleanField("Notificar citas", default = False)
    notifyvia = models.CharField("Notificar por", max_length = 10, choices = modeVia, default = 'Email')
    # Campos de control
    firstupdated = models.DateTimeField("Fecha registro", auto_now_add = True)
    lastupdated = models.DateTimeField("Fecha actualización", auto_now = True)
    modifiedby = models.CharField("Modificado por", max_length = 50, blank = True, default = 'fixuUser')

    def __str__(self):
        return '{}, {}'.format(self.familyname, self.name)

    def get_absolute_url(self):
        return reverse('id-pacientes', args=[self.idPaciente])

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['familyname', 'name']
