import datetime



#########################################
#                                       #
#        FUNCIONES DE PACIENTES         #
#                                       #
#########################################

# Funcion que calcula la edad a partir de la fecha de nacimiento
def calculate_age(birth_date):
    days_in_year = 365.2425
    age = int((datetime.date.today() - birth_date).days / days_in_year)
    return age
