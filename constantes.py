# -*- coding: utf-8 -*-
"""
    Clase para declarar las constantes
"""

# Falta ver que indice es de la tcb
# Hilillos
HILILLO_ID = 0              # Id del hilillo en la TCB
HILILLO_REG = 2             # Pos en la TCB donde estan los registros
HILILLO_ESTADO = 3          # Estado del hilillo en la TCB

# Estados de hilillos
NO_EJECUTADO = 0
EJECUCION = 1
TERMINADO = 2


# Cache de Instrucciones
ID_BLOQUE = 4


#Estados de caché
INVALIDO = -1
VALIDO = 1