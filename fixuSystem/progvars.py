##### VERSION DEL PROGRAMA #####

PROG_VERS = '0.70'

##### CONFIG: VARIABLES DE LA APP GESTION_PACIENTES #####

### Lista de CHOICES para seleccion de ordenacion en el select_pacientes_form ###
selOrder = [
    ('fam', 'Apellidos (por defecto)'),
    ('nam', 'Nombre'),
    ('num', 'DNI'),
    ('idp', 'Paciente ID')
]

### Lista de CHOICES para seleccion de sexo en gestion_pacientes/models.py ###
sexDef = [
    ('No declar.', 'No declar.'),
    ('Masculino', 'Masculino'),
    ('Femenino', 'Femenino'),
    ('Transexual', 'Transexual'),
    ('Bisexual', 'Bisexual'),
    ('Otros', 'Otros')
]

### Lista de CHOICES para seleccion de modos de comunicar las citas en gestion_pacientes/models.py ###
modeVia = [
    ('Email', 'Email'),
    ('Teléfono', 'Teléfono')
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
    ('Pendiente', 'Pendiente'),
    ('Acude', 'Acude'),
    ('Pasa a consulta', 'Pasa a consulta'),
    ('Cancelada', 'Cancelada')
]
##### CONFIG: VARIABLES DE LA APP GESTION_CLINICA #####

##### Choices para el tipo de material/equipamiento #####
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

##### Choices para filtro del tidpo de control
selCtrlEquip = [
    ('oper', 'Operatividad'),
    ('stck', 'Stock'),
]
