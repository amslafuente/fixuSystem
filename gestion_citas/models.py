from django.db import models
from django.urls import reverse
from django.db.models.fields.related import ForeignKey
from gestion_pacientes.models import Paciente
import datetime
from django.forms import ModelChoiceField
from gestion_clinica.models import Profesional, Consultorio
from fixuSystem.progvars import citasStatus

########## TABLA DE GESTION DE CITAS ##########

class Cita(models.Model):

    idCita = models.AutoField(primary_key = True, unique = True)
    # Paciente
    fk_Paciente = models.ForeignKey(Paciente, on_delete = models.PROTECT, related_name = 'pacientes')
    # Fecha y hora
    appdate = models.DateField("Fecha cita", default = datetime.date.today)
    apptime = models.TimeField("Hora cita", default = datetime.time)
    # Citado/a por...
    fk_Profesional = models.ForeignKey(Profesional, on_delete = models.PROTECT, related_name = 'profesionales', blank = True, null = True, limit_choices_to = {'currentavail': True, 'currentstaff': True})
    # En el Consultorio...
    fk_Consultorio = models.ForeignKey(Consultorio, on_delete = models.PROTECT, related_name = 'consultorios', blank = True, null = True, limit_choices_to = {'officeIsavail': True})
    # Estados de la cita: Pendiente, Acudió, Pasa a consulta, Cancelada, Adelantada o Aplazada
    status = models.CharField('Estado cita', max_length = 20, choices = citasStatus, default = 'Pendiente')
    # Notas
    notes = models.TextField('Notas', blank = True)
    # Datos de control
    firstupdated = models.DateTimeField("Fecha registro", auto_now_add = True)
    lastupdated = models.DateTimeField("Fecha actualización", auto_now = True)
    modifiedby = models.CharField("Modificado por", max_length = 50, blank = True, default = 'fixuUser')

    def __str__(self):
        return 'Cita {}/{}'.format(self.idCita, self.fk_Paciente)

    def get_absolute_url(self):
        return reverse('id-citas', args=[self.idCita])

    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['appdate', 'apptime']

########## TABLAS DE PROCESAMIENTO DE CITAS ##########

class NotificaCita(models.Model):

    idNotificaCita = models.AutoField(primary_key = True, unique = True)
    notifLastrun = models.DateTimeField('Ultima fecha de notificación', auto_now = True)
    witherrors = models.BooleanField('Con errores', blank = True, null = True, default = False)
    # Datos de control
    firstupdated = models.DateTimeField("Fecha registro", auto_now_add = True)
    lastupdated = models.DateTimeField("Fecha actualización", auto_now = True)
    modifiedby = models.CharField("Modificado por", max_length = 50, blank = True, default = 'fixuUser')

class ProcesaCita(models.Model):
    
    idProcesaCita = models.AutoField(primary_key = True, unique = True)
    procLastrun = models.DateTimeField('Ultima fecha de procesamiento', auto_now = True)
    # Datos de control
    firstupdated = models.DateTimeField("Fecha registro", auto_now_add = True)
    lastupdated = models.DateTimeField("Fecha actualización", auto_now = True)
    modifiedby = models.CharField("Modificado por", max_length = 50, blank = True, default = 'fixuUser')
