from django.db import models
from django.urls import reverse
from django.db.models.fields.related import ForeignKey
from gestion_pacientes.models import Paciente
from gestion_citas.models import Cita
from gestion_clinica.models import Profesional

########## TABLA DE GESTION DE CONSULTAS ##########

class Consulta(models.Model):

    # ID de consulta
    idConsulta = models.AutoField(primary_key = True, unique = True)
    # OneToOne de la cita
    oto_Cita = models.OneToOneField(Cita, on_delete = models.PROTECT, related_name = 'cita')
    # OneToOne del paciente
    oto_Paciente = models.OneToOneField(Paciente, on_delete = models.PROTECT, related_name = 'paciente')
    # Profesional que trató al paciente
    fk_Profesional = models.ForeignKey(Profesional, on_delete = models.PROTECT, related_name = 'profesional')
    # Campos normales
    age = models.PositiveIntegerField("Edad", blank = True)
    mass = models.PositiveIntegerField("Peso (kg)", blank = True)
    height = models.PositiveIntegerField("Altura (cm)", blank = True)
    familyproblems = models.TextField("Antecedentes familiares", blank = True)
    prevsurgery = models.TextField("Cirugías previas", blank = True)
    alergic = models.TextField("Alergias", blank = True)
    otherpathol = models.TextField("Otras patologías", blank = True)
    physicalexplor = models.TextField("Exploración física", blank = True)
    physicaltest = models.TextField("Pruebas diagnósticas", blank = True)
    diagnostic = models.TextField("Diagnóstico", blank = True)
    medicaltreatm = models.TextField("Tratam. farmacológico", blank = True)
    physicaltreatm = models.TextField("Tratam. físico", blank = True)
    picture1 = models.ImageField("Imagen 1", upload_to = 'consultas/', blank = True)
    picture2 = models.ImageField("Imagen 2", upload_to = 'consultas/', blank = True)
    picture3 = models.ImageField("Imagen 3", upload_to = 'consultas/', blank = True)
    prognosis = models.TextField("Pronóstico", blank = True)
    notes = models.TextField("Notas", blank = True)
    # Estos dos campos se ponen automaticamente
    firstupdated = models.DateTimeField("Fecha consulta", auto_now_add = True)                          # Fecha de registro
    lastupdated = models.DateTimeField("Fecha actualización", auto_now = True)                          # Fecha de la última modificación
    # Este campo se pone programaticamente
    modifiedby = models.CharField("Modificado por", max_length = 50, blank = True, default = 'fixuUser') # Modificad por

    def __str__(self):
        return 'Consulta {}/{}'.format(self.idConsulta, self.fk_Paciente)

    def get_absolute_url(self):
        return reverse('id-consultas/', args=[self.idConsulta])
