from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

########## TABLA DE GESTION DE CLINICA ##########

class Clinica(models.Model):

    idClinica = models.AutoField(primary_key = True)
    dni = models.CharField("DNI", max_length = 9, unique = True)
    nif = models.CharField("NIF", max_length = 25, blank = True, unique = True)
    clinicname = models.CharField("Nombre clínica", max_length = 100)
    ownerfullname = models.CharField("Nombre titular", max_length = 100)
    numcolegiado  = models.CharField("Número colegiado/a", blank = True, max_length = 25, unique = True)
    fulladdress = models.CharField("Dirección completa", max_length = 250)
    postcode = models.PositiveIntegerField("Código postal")
    city = models.CharField("Ciudad", max_length = 50)
    province = models.CharField("Provincia", max_length = 50, blank = True)
    email = models.EmailField("Correo electrónico", max_length = 50)
    phone1 = models.PositiveIntegerField("Teléfono principal")
    phone2 = models.PositiveIntegerField("Teléfono alternativo", null = True, blank = True)
    notes = models.TextField("Notas", blank = True)
    picturefile = models.ImageField('Archivo LOGO', upload_to = 'clinica/', null = True, blank = True)
    # Campos de control
    firstupdated = models.DateTimeField("Fecha registro", auto_now_add = True)
    lastupdated = models.DateTimeField("Fecha actualización", auto_now = True)
    modifiedby = models.CharField("Modificado por", max_length = 50, blank = True, default = 'fixuUser')    # Modificado por

    def __str__(self):
        return self.clinicname

    def get_absolute_url(self):
        return reverse('info-clinica')

    class Meta:
        verbose_name = 'Clínica'
        verbose_name_plural = 'Clínicas'

########## TABLA DE GESTION DE PROFESIONALES ##########

class Profesional(models.Model):

    oto_Profesional = models.OneToOneField(User, on_delete = models.PROTECT, primary_key = True)
    dni = models.CharField("DNI", max_length = 9, unique = True)                                    # DNI
    nif = models.CharField("NIF", max_length = 25, blank = True)                                    # NIF
    fullname = models.CharField("Nombre", max_length = 100)                                         # Nombre y apellidos
    numcolegiado  = models.CharField("Número Colegiado/a", blank = True, max_length = 25)           # Colegiado
    position = models.CharField('Empleo/Puesto/Cargo', max_length = 100)                            # Cargo o puesto
    department = models.CharField('Departamento', max_length = 100, blank = True)                   # Departamento
    fulladdress = models.CharField("Dirección", max_length = 250)                                   # Dirección completa
    postcode = models.PositiveIntegerField("Cód. Postal")                                           # Codigo Postal
    city = models.CharField("Ciudad", max_length = 50)                                              # Ciudad
    province = models.CharField("Provincia", max_length = 50, blank = True)                         # Provincia
    country = models.CharField("País", max_length = 50, blank = True)                               # País
    email2 = models.EmailField("Correo electrónico", max_length = 50)                               # Correo electrónico
    phone1 = models.PositiveIntegerField("Teléfono principal")                                      # Teléfono 1
    phone2 = models.PositiveIntegerField("Teléfono alternativo", blank = True, null = True)         # Teléfono 2
    notes = models.TextField("Notas", blank = True)
    currentavail = models.BooleanField('De alta', default = True)                                                # Notas
    currentstaff = models.BooleanField('En plantilla', default = True)                           # Es personal actual del centro?
    picturefile = models.ImageField(upload_to = 'clinica/', blank = True)                           # Archivo de la foto
    # Campos de control
    firstupdated = models.DateTimeField("Fecha registro", auto_now_add = True)                      # Fecha de registro
    lastupdated = models.DateTimeField("Fecha actualización", auto_now = True)                      # Fecha de la última modificación
    modifiedby = models.CharField("Modificado por", max_length = 50, blank = True, default = 'fixuUser')    # Modificado por

    def __str__(self):
        return self.fullname

    def get_absolute_url(self):
        #return reverse('id-profesional', args=[self.idProfesional])
        pass

    class Meta:
        verbose_name = 'Profesional'
        verbose_name_plural = 'Profesionales'
        ordering = ['fullname']

########## TABLA DE GESTION DE CONSULTORIOS ##########

class Consultorio(models.Model):

    idConsultorio = models.AutoField(primary_key = True, unique = True)
    officeID = models.CharField("Número/Identificación", max_length = 10)
    officeDesc = models.CharField("Descripción", max_length = 100, blank = True)
    officeIsavail = models.BooleanField("Disponible", default = True)                               # Disponible o no para consultas
    officeLocation = models.CharField("Localización", max_length = 50, blank = True)
    officeDepartment = models.CharField("Departamento", max_length = 50, blank = True)
    officeEquipment = models.TextField("Equipamiento", blank = True)
    officePhone = models.PositiveIntegerField("Teléfono consultorio", blank = True, null = True)    # Teléfono 1
    officeNotes = models.TextField("Notas", blank = True)
    # Campos de control
    firstupdated = models.DateTimeField("Fecha registro", auto_now_add = True)                      # Fecha de registro
    lastupdated = models.DateTimeField("Fecha actualización", auto_now = True)                      # Fecha de la última modificación
    modifiedby = models.CharField("Modificado por", max_length = 50, blank = True, default = 'fixuUser')    # Modificado por


    def __str__(self):
        return self.officeID

    def get_absolute_url(self):
        return reverse('id-consultorios', args=[self.idConsultorio])

    class Meta:
        verbose_name = 'Consultorio'
        verbose_name_plural = 'Consultorios'
        ordering =['officeID']