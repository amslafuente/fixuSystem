from .models import Consulta, Antecedente
from gestion_citas.models import Cita
from gestion_pacientes.models import Paciente
from gestion_clinica.models import Profesional



#########################################
#                                       #
#  VARIABLES Y FUNCIONES DE CONSULTAS   #
#                                       #
#########################################

# Crea la ficha vacia del idPaciente para la idCita pasada
def create_fichaconsulta(paciente, cita):

    res = False
    err = ''
    # Si no existe ya una ficha para esa cita...
    try:
        existe_ficha = Consulta.objects.filter(oto_Cita = cita).exists()

        if not existe_ficha:
            ficha = Consulta()

            # Del paciente sale paciente y antecedente
            paciente_ = Paciente.objects.get(idPaciente__exact = paciente)
            ficha.fk_Paciente = paciente_            
            antecedente_ = Antecedente.objects.get(oto_Paciente__exact = paciente_)
            ficha.fk_Antecedente = antecedente_

            # De la cita saco cta y  profesional
            cita_ = Cita.objects.get(idCita__exact = cita)
            ficha.oto_Cita = cita_
            print(cita_)



            ficha.fk_Profesional = cita_.fk_Profesional
            print(ficha.fk_Profesional)                        



            # Pone el modifiedby
            if str(self.request.user) != 'AmonymousUser':
                ficha.modifiedby = str(self.request.user)
            else:
                ficha.modifiedby = 'unix:' + str(self.request.META['USERNAME'])
            # Guarda
            ficha.save()
            res = True
    except Exception as e:
        res = False
        err = e
    print(res)
    print(err)
    return (res, err)

