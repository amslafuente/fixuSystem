import datetime
import locale
from dateutil.relativedelta import relativedelta
from fixuSystem.progvars import START_TIME, END_TIME, TIME_SPAN



#########################################
#                                       #
#     VARIABLES Y FUNCIONES DE CITAS    #
#                                       #
#########################################

# Funcion para extrar valores del dia pasado, el anterior y el siguiente, para pasar al contexto
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

# Funcion para elaborar el grid de citas por franja horaria
def app_timegrid(citas, dia):

    # "citas" pasa cono una lista de tuplas con todas las citas
    # "dia" pasa como un objeto datetime.datetime.date

    # El dia pasado como parametro
    timegrid_day = dia.strftime('%d/%B/%Y')
    timegrid_day_url = dia.strftime('%d_%m_%Y')

    # Hora de comienzo de las consultas. timegrid_ctrl es el puntero de control de la hora que se desplaza con timedelta
    timegrid_start = timegrid_ctrl = datetime.datetime.strptime(timegrid_day + ' ' + START_TIME, '%d/%B/%Y %H:%M')

    # Hora final de las consultas
    timegrid_end = datetime.datetime.strptime(timegrid_day + ' ' + END_TIME, '%d/%B/%Y %H:%M')

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
            if (datetime_cita >= timegrid_ctrl) and (datetime_cita < (timegrid_ctrl + datetime.timedelta(minutes = TIME_SPAN))):
                # Si está, puebla el bloque de TD con esa cita y suma el contador de citas en cada TR
                # cita_row.1/cita.2: Paciente
                # cita_row.2/cita.3: Citado por
                # cita_row.3/cita.4: Consultorio
                # cita_row.5/cita.6: Hora cita 
                # cita_row.7/cita.8: Notas
                # cita_row.6/cita.7: Estado cita
                cada_cita = (timegrid_ctrl, str(cita_row[0]), cita_row[1], str(cita_row[4]), cita_row[5], cita_row[2].strftime('%d/%m/%y'), cita_row[3].strftime('%H:%M'), cita_row[6], cita_row[7])
                datos_citas.append(cada_cita)

        # Siguiente franja horaria
        timegrid_ctrl = timegrid_ctrl + datetime.timedelta(minutes = TIME_SPAN)

    # Devuelve rejilla
    resp = dict()
    resp['franjas_horarias'] = franjas_horarias
    resp['datos_citas'] = datos_citas
    return resp

# Funcion para elaborar el grid de citas por semana y franja horaria
def app_weektimegrid(citas, rango_semana):

    # "citas" pasa cono una lista de tuplas con todas las citas
    # "rango_semana" pasa com tupla con fecha inicial y fecha final

    resp = dict()
    # Set locale
    locale.setlocale(locale.LC_ALL,'es_ES')

    # Date and time appointment distribution

    # Dia de comienzo, puntero de control y final de las consultas
    daygrid_start = daygrid_ctrl = rango_semana[0]
    daygrid_end = rango_semana[1]

    # Hora de comienzo de las consultas, puntero de control de hora y hora final
    timegrid_start = timegrid_ctrl = datetime.datetime.strptime(START_TIME, '%H:%M')
    timegrid_end = datetime.datetime.strptime(END_TIME, '%H:%M')
    timegrid_ctrl2 = timegrid_ctrl + datetime.timedelta(minutes = TIME_SPAN)
    
    # Variable que construye el body
    franjas_horarias = list()
    datos_citas = list()

    """
    for i in franjas horarias
        crea un <tr>
        for j in dias de la semana
            compara cada cita con cada dias de las semana en cada franja horaria
            si existe construye el <td>
            si no existe construye un <td> vacio
    """

    # Construye el body 
    tbl_body = tbl_row = ''
    while timegrid_ctrl.time() <= timegrid_end.time():
       
        tbl_row = tbl_row + '<tr class=\"tr-time-color\">\r<th class=\"tbl-td-centro grid-time-color\">' + timegrid_ctrl.strftime('%H:%M') + '</th>'
        
        daygrid_ctrl = rango_semana[0]
        while daygrid_ctrl <= daygrid_end:

            tbl_row = tbl_row + '<td class=\"grid-smalltxt\">'

            if citas:
                for cita in citas:
                    # Si la cita es de hoy y de esa franja...
                    if (cita[2] == daygrid_ctrl) and (cita[3] >= timegrid_ctrl.time() and cita[3] < timegrid_ctrl2.time()):
                        tbl_row = tbl_row + '<a class=\"grid-smallertxt\" href=\"/fixuSystem/citas/nueva/' + daygrid_ctrl.strftime('%d_%m_%Y') + '/' + timegrid_ctrl.strftime('%H_%M') + '/\">[...]</a>&nbsp;'
                        tbl_row = tbl_row + str(cita[1]) + ' (' + cita[3].strftime('%H:%M') + ')' + ' (' +  str(cita[4])[0].upper() + ')<br/>'
            
            # Pone puntos para crear cita
            tbl_row = tbl_row + '<a class=\"grid-smallertxt\" href=\"/fixuSystem/citas/nueva/' + daygrid_ctrl.strftime('%d_%m_%Y') + '/' + timegrid_ctrl.strftime('%H_%M') + '/\">[...]</a>'
            tbl_row = tbl_row + '</td>'
            daygrid_ctrl = daygrid_ctrl + datetime.timedelta(days = 1)
        
        tbl_row = tbl_row + '</tr>\r'
        timegrid_ctrl = timegrid_ctrl + datetime.timedelta(minutes = TIME_SPAN)
        timegrid_ctrl2 = timegrid_ctrl + datetime.timedelta(minutes = TIME_SPAN)
    
    tbl_body = tbl_row
    
    # Construye header    
    tbl_header = '<tr>\r<th class=\"tbl-th\">Franja horaria</th>\r'
    for i in range(0,7):
        weekday_ = rango_semana[0] + datetime.timedelta(days = i)
        tbl_header = tbl_header + '<th class=\"tbl-th tbl-td-12\">' + weekday_.strftime('%A') + '<br/>' + weekday_.strftime('%d/%b/%y')+ '</th>\r'
    tbl_header = tbl_header + '<tr><td class=\"grid-info2-color tr-time-color tbl-td-centro\" colspan=\"8\">Pulse sobre los puntos de las celdas para crear nuevas citas</td>'
    tbl_header = tbl_header + '</tr>\r'
    
    resp['weekgrid'] = tbl_header + tbl_body

    # Reset locale
    locale.resetlocale(category = locale.LC_ALL)

    return resp


# Funcion para devolver el rango de fechas de una semana completa
def get_weekrange(day_): # "day" es un datetime.date

    weektoday = day_.isocalendar() # isocalendar(year, week, weekday)
    weekstart = day_ - datetime.timedelta(days = weektoday[2] - 1)
    weekend = day_ + datetime.timedelta(days = 7 - weektoday[2])
    return (weekstart, weekend)

# Funcion para elaborar el grid de citas por mes y franja horaria
def app_monthtimegrid(citas, dia):

    # "citas" pasa cono una lista de tuplas con todas las citas
    # "dia" pasa como un objeto datetime.datetime.date

    pass