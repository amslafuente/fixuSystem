import datetime
from dateutil.relativedelta import relativedelta
from fixuSystem.progvars import HORA_COMIENZO, HORA_FINAL, DURACION_CONSULTA

########## VARIABLES Y FUNCIONES GLOBALES PARA USAR ##########

##### Funcion para extrar valores del dia pasado, el anterior y el siguiente, para pasar al contexto

def contexto_dias(dia):

    ctx_dias = dict()

    ctx_dias['current_date'] = dia
    ctx_dias['tomorrow'] = dia + datetime.timedelta(days = 1)
    ctx_dias['yesterday'] = dia + datetime.timedelta(days = -1)
    ctx_dias['week_forw'] = dia + datetime.timedelta(weeks = 1)
    ctx_dias['week_back'] = dia + datetime.timedelta(weeks = -1)
    ctx_dias['month_forw'] = dia + relativedelta(months = +1)
    ctx_dias['month_back'] = dia + relativedelta(months = -1)

    ctx_dias['current_date_y'] = ctx_dias['current_date'].strftime('%Y')
    ctx_dias['current_date_m'] = ctx_dias['current_date'].strftime('%m')
    ctx_dias['current_date_d'] = ctx_dias['current_date'].strftime('%d')
    ctx_dias['current_date_url'] = ctx_dias['current_date'].strftime('%d_%m_%Y')

    ctx_dias['tomorrow_y'] = ctx_dias['tomorrow'].strftime('%Y')
    ctx_dias['tomorrow_m'] = ctx_dias['tomorrow'].strftime('%m')
    ctx_dias['tomorrow_d'] = ctx_dias['tomorrow'].strftime('%d')
    ctx_dias['tomorrow_url'] = ctx_dias['tomorrow'].strftime('%d_%m_%Y')

    ctx_dias['yesterday_y'] = ctx_dias['yesterday'].strftime('%Y')
    ctx_dias['yesterday_m'] = ctx_dias['yesterday'].strftime('%m')
    ctx_dias['yesterday_d'] = ctx_dias['yesterday'].strftime('%d')
    ctx_dias['yesterday_url'] = ctx_dias['yesterday'].strftime('%d_%m_%Y')

    ctx_dias['week_forw_y'] = ctx_dias['week_forw'].strftime('%Y')
    ctx_dias['week_forw_m'] = ctx_dias['week_forw'].strftime('%m')
    ctx_dias['week_forw_d'] = ctx_dias['week_forw'].strftime('%d')
    ctx_dias['week_forw_url'] = ctx_dias['week_forw'].strftime('%d_%m_%Y')

    ctx_dias['week_back_y'] = ctx_dias['week_back'].strftime('%Y')
    ctx_dias['week_back_m'] = ctx_dias['week_back'].strftime('%m')
    ctx_dias['week_back_d'] = ctx_dias['week_back'].strftime('%d')
    ctx_dias['week_back_url'] = ctx_dias['week_back'].strftime('%d_%m_%Y')

    ctx_dias['month_forw_y'] = ctx_dias['month_forw'].strftime('%Y')
    ctx_dias['month_forw_m'] = ctx_dias['month_forw'].strftime('%m')
    ctx_dias['month_forw_d'] = ctx_dias['month_forw'].strftime('%d')
    ctx_dias['month_forw_url'] = ctx_dias['month_forw'].strftime('%d_%m_%Y')

    ctx_dias['month_back_y'] = ctx_dias['month_back'].strftime('%Y')
    ctx_dias['month_back_m'] = ctx_dias['month_back'].strftime('%m')
    ctx_dias['month_back_d'] = ctx_dias['month_back'].strftime('%d')
    ctx_dias['month_back_url'] = ctx_dias['month_back'].strftime('%d_%m_%Y')

    # Devuelve un dict de fechas
    return ctx_dias

########## FUNCION PARA ELABORAR EL GRID DE CITAS POR FRANJA HORARIA ##########

def app_timegrid(citas, dia):

    # "citas" pasa cono una lista de tuplas con todas las citas
    # "dia" pasa como un objeto datetime.datetime.date

    # El dia pasado como parametro
    timegrid_day = dia.strftime('%d/%B/%Y')
    timegrid_day_url = dia.strftime('%d_%m_%Y')

    # Hora de comienzo de las consultas. timegrid_ctrl es la ora que se desplaza con timedelta
    timegrid_start = timegrid_ctrl = datetime.datetime.strptime(timegrid_day + ' ' + HORA_COMIENZO, '%d/%B/%Y %H:%M')

    # Hora final de las consultas
    timegrid_end = datetime.datetime.strptime(timegrid_day + ' ' + HORA_FINAL, '%d/%B/%Y %H:%M')

    # Variable que construye el body
    franjas_horarias = list()
    datos_citas = list()

    # Pasa por todas las franjas horarias
    while timegrid_ctrl <= timegrid_end:

        # Añade la hora de la franja por la que va pasando y suma 1 al numero de franjas
        # Formato para el grid y para la URL
        franjas_horarias.append(timegrid_ctrl)

        # Recorre la matriz de citas
        for cita in range(0, len(citas)):

            # Extrae cada fila (cada cita)
            cita_row = citas[cita]

            # Combina dia y hora de cada cita
            datetime_cita = datetime.datetime.combine(cita_row[2], cita_row[3])

            # Comprueba si ese dia y hora están en la franja horaria actual
            if (datetime_cita >= timegrid_ctrl) and (datetime_cita < (timegrid_ctrl + datetime.timedelta(minutes = DURACION_CONSULTA))):
                # Si está, puebla el bloque de TD con esa cita y suma el contador de citas en cada TR
                cada_cita = (timegrid_ctrl, str(cita_row[0]), cita_row[1], str(cita_row[4]), cita_row[5], cita_row[2].strftime('%d/%m/%y'), cita_row[3].strftime('%H:%M'), cita_row[6], cita_row[7])
                datos_citas.append(cada_cita)

        # Siguiente franja horaria
        timegrid_ctrl = timegrid_ctrl + datetime.timedelta(minutes = DURACION_CONSULTA)

    # Devuelve rejilla
    resp = dict()
    resp['franjas_horarias'] = franjas_horarias
    resp['datos_citas'] = datos_citas
    return resp
