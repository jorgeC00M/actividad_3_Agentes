# src/config/parametros.py

# Configuración Ejercicio 1: Agente con memoria
CONFIG_EJERCICIO_1 = {
    "ancho_grid": 6,
    "alto_grid": 6,
    "num_suciedad": 10,
    "max_pasos": 40,
    "posicion_agente": (3, 3),
}

# Configuración Ejercicio 2: Tipos de suciedad
CONFIG_EJERCICIO_2 = {
    "ancho_grid": 5,
    "alto_grid": 5,
    "num_suciedad": 12,
    "max_pasos": 30,
    "posicion_agente": (2, 2),
}

# Configuración Ejercicio 3: Evasión de obstáculos
CONFIG_EJERCICIO_3 = {
    "ancho_grid": 8,
    "alto_grid": 8,
    "num_suciedad": 15,
    "num_obstaculos": 12,
    "max_pasos": 50,
    "posicion_agente": (4, 4),
}

# Configuración Ejercicio 4: Comunicación entre agentes
CONFIG_EJERCICIO_4 = {
    "ancho_grid": 10,
    "alto_grid": 10,
    "num_comida": 15,
    "num_obstaculos": 8,
    "num_agentes": 3,
    "max_pasos": 60,
}

# Configuración Ejercicio 5: Memoria espacial
CONFIG_EJERCICIO_5 = {
    "ancho_grid": 8,
    "alto_grid": 8,
    "num_comida": 16,
    "num_obstaculos": 6,
    "max_pasos": 60,
    "posicion_agente": (0, 0),
}

# Configuración Ejercicio 6: Sistema competitivo
CONFIG_EJERCICIO_6 = {
    "ancho_grid": 12,
    "alto_grid": 12,
    "num_comida": 10,  # Pocos recursos para competencia
    "num_obstaculos": 10,
    "num_agentes": 4,
    "max_pasos": 80,
    "estrategias": ["agresiva", "conservadora", "evasiva", "agresiva"],
}
