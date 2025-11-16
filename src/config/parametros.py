"""Parámetros de configuración de las simulaciones."""

# Configuración de entornos
CONFIG_LIMPIEZA = {
    'ancho': 10,
    'alto': 10,
    'num_suciedad': 15,
    'num_obstaculos': 5,
    'tipos_suciedad': True
}

CONFIG_RECOLECCION = {
    'ancho': 15,
    'alto': 15,
    'num_comida': 20,
    'num_agentes': 3
}

CONFIG_COMPETITIVO = {
    'ancho': 12,
    'alto': 12,
    'num_comida': 15,
    'num_agentes': 4,
    'competitivo': True
}

# Configuración de simulación
PASOS_SIMULACION = 50
MOSTRAR_CADA = 10
USAR_VISUALIZACION = True