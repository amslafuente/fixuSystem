##### VERSION DEL PROGRAMA #####

PROG_VERS = '0.75'

##### CONFIG: VARIABLES DE LA APP GESTION_PACIENTES #####

# Lista de CHOICES para seleccion de ordenacion en el select_pacientes_form
# List of CHOICES to select record ordering in select_pacientes_form
# The first item of each pair (eg. nam) is inmutable, but you can customise the second (ie. Name instead of Nombre)
selOrder = [
    ('fam', 'Apellidos (por defecto)'),
    ('nam', 'Nombre'),
    ('num', 'DNI'),
    ('idp', 'Paciente ID')
]

# Lista de CHOICES para seleccion de sexo en gestion_pacientes/models.py
# List of CHOICES to select patients' sex
# The first item of each pair (eg. fem) is inmutable, but you can customise the second (ie. Female instead of Femenino)
sexDef = [
    ('und', 'No declarado'),
    ('mal', 'Masculino'),
    ('fem', 'Femenino'),
    ('oth', 'Otros')
]

# Lista de CHOICES para seleccion de modos de comunicar las citas en gestion_pacientes/models.py ###
# List of CHOICES to select how appointments should be notified
# The first item of each pair is inmutable, but you can customise the second
modeVia = [
    ('eml', 'Email'),
    ('phn', 'Teléfono')
]

##### CONFIG: VARIABLES DE LA APP GESTION_CITAS #####

# Hora de comienzo de las consultas en formato string: HH:MM
START_TIME = '13:00'

# Hora de finalización de las consultas en formato string: HH:MM
END_TIME = '19:30'

# Duración en MINUTOS aproximada de cada ventana de consulta int: N
TIME_SPAN = 30

# Notificar citas con ESTOS dias de antelación int: N
NOTIFICAR_CON = 3

##### Choices para el status de las citas #####
citasStatus = [
    ('pen', 'Pendiente'),
    ('att', 'Acude'),
    ('exm', 'Pasa a consulta'),
    ('cnl', 'Cancelada')
]
##### CONFIG: VARIABLES DE LA APP GESTION_CLINICA #####

# Lista de CHOICES para seleccion del tipo de equipamiento
# List of CHOICES to select equipment types
# Both items of each pair ar fully customisable, and can be adapted to your own needs
selTipoEquip = [
    ('infor', 'Equipos informáticos'),
    ('muscl', 'Máquinas musculación'),
    ('eqtrm', 'Equipos tratamiento'),
    ('enfer', 'Enfermería'),
    ('fung', 'Fungible'),
    ('mobi', 'Mobiliario'),
    ('papel', 'Papelería'),    
    ('limp', 'Limpieza'),
    ('otros', 'Otros'),
]

# Lista de CHOICES para seleccion del control del equipamiento
# List of CHOICES to select equipment conrol
# The first item of each pair is inmutable, but you can customise the second
selCtrlEquip = [
    ('ope', 'Operatividad'),
    ('stk', 'Stock'),
]
