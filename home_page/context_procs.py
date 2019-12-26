from .models import Clinica
from fixuSystem.progvars import PROG_VERS

########## FUNCIONES GLOBALES ##########

# Devuelve version del programa
def get_prog_vers(request):
    pg = dict()
    pg['progvers'] = PROG_VERS
    return pg

# Devuelve los datos de la clinica en el contexto
def get_datos_clinica(request):
    # Recupera el registro 1 de la clinica
    clinica= dict()
    try:
        clinica['clinica'] = Clinica.objects.first()
    except:
        clinica['clinica'] = None
    return clinica
