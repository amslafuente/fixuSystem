from .models import Consulta, Antecedente
from gestion_citas.models import Cita
from gestion_pacientes.models import Paciente
from gestion_clinica.models import Profesional
from gestion_pacientes.funct import calculate_age



#########################################
#                                       #
#  VARIABLES Y FUNCIONES DE CONSULTAS   #
#                                       #
#########################################

# Crea la ficha vacia de consulta para la idCita pasada
def create_fichaconsulta(request, cita):

    res = False
    err = ''
    # Si no existe ya una ficha para esa cita...
    try:
        existe_ficha = Consulta.objects.filter(oto_Cita = cita).exists()
      
        if not existe_ficha:
            ficha = Consulta()

            # Recupera los datos de cita
            cita_ = Cita.objects.get(idCita__exact = cita)
  
            # Establece fk_Paciente
            paciente_ = Paciente.objects.get(idPaciente__exact = cita_.fk_Paciente.idPaciente)
            ficha.fk_Paciente = paciente_            

            # Establece fk_Antecedente            
            antecedente_ = Antecedente.objects.get(oto_Paciente__exact = paciente_)
            ficha.fk_Antecedente = antecedente_
            
            # Establece oto_cita
            ficha.oto_Cita = cita_
            
            # Si el la cita hay profesional asignado establece el fk_Profesional
            if cita_.fk_Profesional:
                ficha.fk_Profesional = cita_.fk_Profesional
            else:
                ficha.fk_Profesional = None

            # Calcula la edad del paciente
            ficha.age = calculate_age(paciente_.birthdate)
            
            # Pone el modifiedby
            if str(request.user) != 'AmonymousUser':
                ficha.modifiedby = str(request.user)
            else:
                ficha.modifiedby = 'unix:' + str(request.META['USERNAME'])
            # Guarda
            ficha.save()
            res = True
            # Cambia el estatus de la cita
            if res:
                try:
                    cita_.status = 'exm'
                    cita_.save()
                except Exception as e:
                    res = False
                    err = e
                return (res, err)
    except Exception as e:
        res = False
        err = e
    return (res, err)

