from django.db import models
from django.urls import reverse
from django.db.models.fields.related import ForeignKey
from gestion_pacientes.models import Paciente
from gestion_citas.models import Cita
from gestion_clinica.models import Profesional



#########################################
#                                       #
#         TABLA DE ANTEDECENTES         #
#                                       #
#########################################

class Antecedente(models.Model):

    # OneToOne al paciente
    oto_Paciente = models.OneToOneField(Paciente, on_delete = models.PROTECT, related_name = 'antecedpaciente', primary_key = True, unique = True)
    
    familyproblems = models.TextField("Antecedentes familiares", blank = True)
    prevsurgery = models.TextField("Cirugías previas", blank = True)
    alergic = models.TextField("Alergias", blank = True)
    otherpathol = models.TextField("Otras patologías", blank = True)

    # Campos de control
    firstupdated = models.DateTimeField("Fecha creación", auto_now_add = True)                
    lastupdated = models.DateTimeField("Fecha actualización", auto_now = True)                      
    modifiedby = models.CharField("Modificado por", max_length = 50, blank = True, default = 'fixuUser') 
    
    def __str__(self):
        return 'Antecedentes {}/{}'.format(self.idAntecedente, self.fk_Paciente)

    def get_absolute_url(self):
        return reverse('id-antecedente/', args=[self.idAntecedente])



#########################################
#                                       #
#         TABLA DE CONSULTAS            #
#                                       #
#########################################

class Consulta(models.Model):

    idConsulta = models.AutoField(primary_key = True, unique = True)

    # OneToOne de la cita
    oto_Cita = models.OneToOneField(Cita, on_delete = models.PROTECT, related_name = 'cita')
    # Foreignkey del paciente
    fk_Paciente = models.ForeignKey(Paciente, on_delete = models.PROTECT, related_name = 'paciente')
    # Foreignkey del antecedentes
    fk_Antecedente = models.ForeignKey(Antecedente, on_delete = models.PROTECT, related_name = 'antecedentes')
    # Profesional que trató al paciente
    fk_Profesional = models.ForeignKey(Profesional, on_delete = models.PROTECT, related_name = 'profesional')

    age = models.PositiveIntegerField("Edad", blank = True)
    mass = models.PositiveIntegerField("Peso (kg)", blank = True)
    height = models.PositiveIntegerField("Altura (cm)", blank = True)
    physicalexplor = models.TextField("Exploración física", blank = True)
    physicaltest = models.TextField("Pruebas diagnósticas", blank = True)
    diagnostic = models.CharField("Diagnóstico", max_length = 250, blank = True)
    medicaltreatm = models.CharField("Tratam. farmacológico", max_length = 250, blank = True)
    physicaltreatm = models.CharField("Tratam. físico", max_length = 250, blank = True)
    prognosis = models.TextField("Pronóstico", blank = True)
    picture1 = models.ImageField("Imagen 1", upload_to = 'consultas/', blank = True)
    picture2 = models.ImageField("Imagen 2", upload_to = 'consultas/', blank = True)
    picture3 = models.ImageField("Imagen 3", upload_to = 'consultas/', blank = True)
    notes = models.TextField("Notas", blank = True)
 
    # Campos de control
    firstupdated = models.DateTimeField("Fecha creación", auto_now_add = True)                          # Fecha de registro
    lastupdated = models.DateTimeField("Fecha actualización", auto_now = True)                          # Fecha de la última modificación
    modifiedby = models.CharField("Modificado por", max_length = 50, blank = True, default = 'fixuUser') # Modificad por

    def __str__(self):
        return 'Consulta {}/{}'.format(self.idConsulta, self.fk_Paciente)

    def get_absolute_url(self):
        return reverse('id-consultas/', args=[self.idConsulta])
