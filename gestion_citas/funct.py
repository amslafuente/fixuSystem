import datetime
import locale
from dateutil.relativedelta import relativedelta
from fixuSystem.progvars import START_TIME, END_TIME, TIME_SPAN
from django.shortcuts import reverse
from django.urls import reverse_lazy    
from weasyprint import HTML    
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string



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
def app_daytimegrid(citas, dia, paciente):

    # "citas" pasa cono una lista de tuplas con todas las citas
    # "dia" pasa como datetime.date

    resp = dict()
    # Set locale
    locale.setlocale(locale.LC_ALL,'es_ES')

    # Time appointment distribution

    # Hora de comienzo de las consultas, puntero de control de hora y hora final
    timegrid_start = timegrid_ctrl = datetime.datetime.strptime(START_TIME, '%H:%M')
    timegrid_end = datetime.datetime.strptime(END_TIME, '%H:%M')
    timegrid_ctrl2 = timegrid_ctrl + datetime.timedelta(minutes = TIME_SPAN)
 
    # Construye el body 
    tbl_body = tbl_row = ''

    """
    for i in franjas horarias
        crea un <tr>
            compara cada cita con de ese dia en cada franja horaria
            si existe construye el <td>
            si no existe construye un <td> vacio
    """

    while timegrid_ctrl.time() <= timegrid_end.time():
           
        tbl_row = tbl_row + '<tr class=\"tr-time-color\">\r'
        tbl_row = tbl_row + '<th class=\"tbl-td-centro grid-time-color\">'

        # Si se pasa un paciente lo incluye en el enlace para crear citas
        if paciente[0] > 0:
            data = dict()
            data['idPaciente'] = int(paciente[0])
            data['date'] = dia.strftime('%d_%m_%Y')
            data['hour'] = timegrid_ctrl.strftime('%H_%M') 
            link = reverse('create-citas-paciente', kwargs = data)
            tbl_row = tbl_row + '<a href=\"' + link + '\">' + timegrid_ctrl.strftime('%H:%M') + '</a>'
        # Si no, solo enlace con dia y hora
        else:
            data = dict()
            data['date'] = dia.strftime('%d_%m_%Y')
            data['hour'] = timegrid_ctrl.strftime('%H_%M') 
            link = reverse('create-citas', kwargs = data)
            tbl_row = tbl_row + '<a href=\"' + link + '\">' + timegrid_ctrl.strftime('%H:%M') + '</a>'
        
        tbl_row = tbl_row + '</th>\r'

        if citas:
            # Pacientes
            tbl_row = tbl_row + '<td class=\"grid-smalltxt\">'
            for cita in citas:
                # Si la cita es de hoy y de esa franja...
                    if (cita[3] >= timegrid_ctrl.time() and cita[3] < timegrid_ctrl2.time()):
                        if cita[6] == 'Cancelada':
                            tbl_row = tbl_row + '<span class=\"grid-tachado\">'
                        else:
                            tbl_row = tbl_row + '<span>'
                        tbl_row = tbl_row + str(cita[1]) + '</span><br/>'
            tbl_row = tbl_row + '</td>'            
            # Citado por
            tbl_row = tbl_row + '<td class=\"grid-smalltxt\">'
            for cita in citas:
                # Si la cita es de hoy y de esa franja...
                    if (cita[3] >= timegrid_ctrl.time() and cita[3] < timegrid_ctrl2.time()):
                        if cita[6] == 'Cancelada':
                            tbl_row = tbl_row + '<span class=\"grid-tachado\">'
                        else:
                            tbl_row = tbl_row + '<span>'
                        if not cita[4]:
                            tbl_row = tbl_row + 'Indet.</span><br/>'
                        else:
                            tbl_row = tbl_row + str(cita[4]) + '</span><br/>'
            tbl_row = tbl_row + '</td>'            
            # Consultorio
            tbl_row = tbl_row + '<td class=\"tbl-td-centro grid-smalltxt\">'
            for cita in citas:
                # Si la cita es de hoy y de esa franja...
                    if (cita[3] >= timegrid_ctrl.time() and cita[3] < timegrid_ctrl2.time()):
                        if cita[6] == 'Cancelada':
                            tbl_row = tbl_row + '<span class=\"grid-tachado\">'
                        else:
                            tbl_row = tbl_row + '<span>'
                        if not cita[5]:
                            tbl_row = tbl_row + 'Indet.</span><br/>'
                        else:
                            tbl_row = tbl_row + str(cita[5]) + '</span><br/>'
            tbl_row = tbl_row + '</td>'            
            # Hora real
            tbl_row = tbl_row + '<td class=\"tbl-td-centro grid-smalltxt\">'
            for cita in citas:
                # Si la cita es de hoy y de esa franja...
                    if (cita[3] >= timegrid_ctrl.time() and cita[3] < timegrid_ctrl2.time()):
                        if cita[6] == 'Cancelada':
                            tbl_row = tbl_row + '<span class=\"grid-tachado\">'
                        else:
                            tbl_row = tbl_row + '<span>'
                        tbl_row = tbl_row + cita[3].strftime('%H:%M') + '</span><br/>'
            tbl_row = tbl_row + '</td>'            
            # Notas
            tbl_row = tbl_row + '<td class=\"tbl-td-20 grid-smalltxt\">'
            for cita in citas:
                # Si la cita es de hoy y de esa franja...
                    if (cita[3] >= timegrid_ctrl.time() and cita[3] < timegrid_ctrl2.time()):
                        if cita[6] == 'Cancelada':
                            tbl_row = tbl_row + '<span class=\"grid-tachado\">'
                        else:
                            tbl_row = tbl_row + '<span>'
                        tbl_row = tbl_row + cita[7] + '</span><br/>'
            tbl_row = tbl_row + '</td>'            
            # Estado
            tbl_row = tbl_row + '<td class=\"tbl-td-centro grid-smalltxt\">'
            for cita in citas:
                # Si la cita es de hoy y de esa franja...
                    if (cita[3] >= timegrid_ctrl.time() and cita[3] < timegrid_ctrl2.time()):
                        if cita[6] == 'Cancelada':
                            tbl_row= tbl_row + '<span class=\"grid-rojo\">'
                        elif cita[6] == 'Acude':
                            tbl_row = tbl_row + '<span class=\"grid-azul\">'
                        elif cita[6] == 'Pendiente':
                            tbl_row = tbl_row + '<span class=\"grid-naranja\">'
                        else:
                            tbl_row = tbl_row + '<span class=\"grid-verde\">'
                        tbl_row = tbl_row + cita[6] + '</span><br/>'
            tbl_row = tbl_row + '</td>\r'
            # Acciones
            tbl_row = tbl_row + '<td class=\"tbl-td-centro grid-smalltxt\">'
            for cita in citas:
                # Si la cita es de hoy y de esa franja...
                    if (cita[3] >= timegrid_ctrl.time() and cita[3] < timegrid_ctrl2.time()):
                        if (cita[6] != "Cancelada" and cita[6] != "Pasa a consulta"):
                            data = dict()
                            data['idCita'] = int(cita[0])
                            link = reverse('cancel-citas', kwargs = data)
                            tbl_row = tbl_row + '<a class=\"link-cancelar\" href=\"' + link + '\">Cancelar cita</a><br/>'
                        else:
                            tbl_row = tbl_row + '<span>&nbsp;</span><br/>'
            tbl_row = tbl_row + '</td>\r'
        
        tbl_row = tbl_row + '</tr>\r'            
        timegrid_ctrl = timegrid_ctrl + datetime.timedelta(minutes = TIME_SPAN)
        timegrid_ctrl2 = timegrid_ctrl + datetime.timedelta(minutes = TIME_SPAN)
    
    tbl_body = tbl_row

    # Construye header    
    tbl_header = '<tr>\r'
    tbl_header = tbl_header + '<th class=\"tbl-th\">Franja horaria</th>\r'
    tbl_header = tbl_header + '<th class=\"tbl-th-izq tbl-td-20\">Paciente</th>\r'
    tbl_header = tbl_header + '<th class=\"tbl-th-izq tbl-td-15\">Citado/a por</th>\r'
    tbl_header = tbl_header + '<th class=\"tbl-th\">Consult.</th>\r'
    tbl_header = tbl_header + '<th class=\"tbl-th\">Hora</th>\r'
    tbl_header = tbl_header + '<th class=\"tbl-th-izq\">Notas</th>\r'
    tbl_header = tbl_header + '<th class=\"tbl-th tbl-td-15\">Estado</th>\r'
    tbl_header = tbl_header + '<th class=\"tbl-th\">Acciones</th>\r'
    tbl_header = tbl_header + '</tr>\r'
    # Si se pasa un paciente lo coloca en la cabecera
    if paciente[0] > 0:
        tbl_header = tbl_header + '<tr>\r<td class=\"grid-info-color tr-time-color tbl-td-centro\" colspan=\"8\"> Paciente: ' + paciente[1] + '</td>\r</tr>\r'
    # Pulsacion para nuevas citas
    tbl_header = tbl_header + '<tr>\r<td class=\"grid-info2-color tr-time-color tbl-td-centro\" colspan=\"8\">Pulse sobre las franjas horarias para crear nuevas citas</td>\r</tr>\r'

    resp['daygrid'] = tbl_header + tbl_body

    # Reset locale
    locale.resetlocale(category = locale.LC_ALL)

    return resp

# Funcion para elaborar el grid de citas por semana y franja horaria
def app_weektimegrid(citas, rango_semana):

    # "citas" pasa cono una lista de tuplas con todas las citas
    # "rango_semana" pasa como tupla con fecha inicial y fecha final

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
       
        tbl_row = tbl_row + '<tr class=\"tr-time-color\">\r'
        tbl_row = tbl_row + '<th class=\"tbl-td-centro grid-time-color\">' + timegrid_ctrl.strftime('%H:%M') + '</th>\r'
        
        daygrid_ctrl = rango_semana[0]
        while daygrid_ctrl <= daygrid_end:

            tbl_row = tbl_row + '<td class=\"grid-smallertxt\">'

            if citas:
                for cita in citas:
                    # Si la cita es de hoy y de esa franja...
                    if (cita[2] == daygrid_ctrl) and (cita[3] >= timegrid_ctrl.time() and cita[3] < timegrid_ctrl2.time()):
                        # Si la cita está cancelada...
                        if cita[4] == 'Cancelada':
                            tbl_row = tbl_row + '<span class=\"grid-tachado\">' + cita[3].strftime('%H:%M') + '. ' + str(cita[1]) + ' (' +  cita[4] + ')</span><br/>'    
                        else:
                            tbl_row = tbl_row + cita[3].strftime('%H:%M') + '. ' + str(cita[1]) + ' (' +  cita[4] + ')<br/>'
            
            # Pone puntos para crear cita
            data = dict()
            data['date'] = daygrid_ctrl.strftime('%d_%m_%Y')
            data['hour'] = timegrid_ctrl.strftime('%H_%M')
            link = reverse('create-citas', kwargs = data) 
            tbl_row = tbl_row + '<a class=\"grid-smallertxt\" href=\"' + link + '\">[...]</a>'
            tbl_row = tbl_row + '</td>\r'
            daygrid_ctrl = daygrid_ctrl + datetime.timedelta(days = 1)        
        
        tbl_row = tbl_row + '</tr>\r'
        timegrid_ctrl = timegrid_ctrl + datetime.timedelta(minutes = TIME_SPAN)
        timegrid_ctrl2 = timegrid_ctrl + datetime.timedelta(minutes = TIME_SPAN)
    
    tbl_body = tbl_row
    
    # Construye header    
    tbl_header = '<tr>\r'
    tbl_header = tbl_header + '<th class=\"tbl-th\">Franja<br/>horaria</th>\r'
    for i in range(0,7):
        weekday_ = rango_semana[0] + datetime.timedelta(days = i)
        # Si es hoy lo pone en rojo
        if weekday_ == datetime.date.today():
            tbl_header = tbl_header + '<th class=\"tbl-th-dark tbl-td-12\">' + weekday_.strftime('%A') + '<br/>' + weekday_.strftime('%d/%b/%y')+ '</th>\r'            
        else:
            tbl_header = tbl_header + '<th class=\"tbl-th tbl-td-12\">' + weekday_.strftime('%A') + '<br/>' + weekday_.strftime('%d/%b/%y')+ '</th>\r'
    tbl_header = tbl_header + '</tr>\r'
    tbl_header = tbl_header + '<tr>\r<td class=\"grid-info2-color tr-time-color tbl-td-centro\" colspan=\"8\">Pulse sobre los puntos de las celdas para crear nuevas citas</td>\r</tr>\r'
    
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

# Funcion para general un PDF de las citas a notifiar por telefono
def html2pdf(restelef, emails2phone, notifydate, untilday):

    # Construye la tabla HTML con los datos pasados (restelef y emails2phone)
    html_table = ''

    html_table = html_table + '<table class="tbl-forms table-striped tbl-general tbl-85">' 
    html_table = html_table + '<caption class="tbl-capt">Notificaciones a hacer por teléfono</caption>'
    html_table = html_table + '<tr><th class="tbl-th" colspan="3">Citas para el día ' + notifydate + ' ' + untilday + '</th></tr>'
    
    if restelef == '':
        html_table = html_table + '<tr><th colspan="3" class="field-errors"><span>Ninguna cita a notificar</span></th></tr>'
    else:  
        for telef in range(len(restelef)):
            html_table = html_table + '<tr><td colspan="3"><hr/></td></tr>'
            html_table = html_table + '<tr><th>Paciente</th><th>Telef.1</th><th>Telef.2</th></tr>'
            html_table = html_table + '<tr><td>' + restelef[telef][1] + ',<br/>' + restelef[telef][2] + '</td><td>' + restelef[telef][3] + '</td><td>' + restelef[telef][4] + '</td></tr>'
            html_table = html_table + '<tr><th class="tbl-td-centro">Notificada</th><th class="tbl-td-centro">Fecha cita</th><th class="tbl-td-centro">Hora cita</th></tr>'
            html_table = html_table + '<tr><td><div style="width: 12px; height:12px; border: 1px solid #000;">&nbsp;</div></td><td>' + restelef[telef][7] + '/' + restelef[telef][6] + '/' +restelef[telef][5] + '</td><td>' + restelef[telef][8] + ':' + restelef[telef][9]       + '</td></tr>'
        html_table = html_table + '<tr><td colspan="3"><hr/></td></tr>'

    if emails2phone != '':
        html_table = html_table + '<tr><th colspan="3" class="field-errors"><span>Citas a notificar por teléfono por errores en el envío de email</span></th></tr>'
        for telef in range(len(emails2phone)):
            html_table = html_table + '<tr><td colspan="3"><hr/></td></tr>'
            html_table = html_table + '<tr><th>Paciente</th><th>Telef.1</th><th>Telef.2</th></tr>'
            html_table = html_table + '<tr><td>' + restelef[telef][1] + ',<br/>' + restelef[telef][2] + '</td><td>' + restelef[telef][3] + '</td><td>' + restelef[telef][4] + '</td></tr>'
            html_table = html_table + '<tr><th class="tbl-td-centro">Notificada</th><th class="tbl-td-centro">Fecha cita</th><th class="tbl-td-centro">Hora cita</th></tr>'
            html_table = html_table + '<tr><td><div style="width: 12px; height:12px; border: 1px solid #000;">&nbsp;</div></td><td>' + restelef[telef][7] + '/' + restelef[telef][6] + '/' +restelef[telef][5] + '</td><td>' + restelef[telef][8] + ':' + restelef[telef][9]       + '</td></tr>'
        html_table = html_table + '<tr><td colspan="3"><hr/></td></tr>'

    html_table = html_table + '</table>'

    html_string = render_to_string('recordatorios_pdf_citas_tpl.html')

    # html = HTML(string=html_string)
    filename = ('Notificaciones_' + notifydate + '.pdf').replace(' de ', '_')
    html = HTML(string = html_table)
    html.write_pdf(target = '/tmp/' + filename);

    fs = FileSystemStorage('/tmp')
    with fs.open(filename) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename = ' + filename

    return response
    