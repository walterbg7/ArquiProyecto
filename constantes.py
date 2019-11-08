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


# Caches
ID_BLOQUE = 4
ESTADO_BLOQUE = 5

#Estados de caché
INVALIDO = -1
VALIDO = 1

# Intrucciones
LW = 5
ADDI = 19
SW = 37
DIV = 56
ADD = 71
MUL = 72
SUB = 83
BEQ = 99
BNE = 100
JAR = 103
JALR = 111
FIN = 999


# Para saber si los hilillos ya terminaron
NINGUNO = 0 # NO HAY HILILLOS TERMINADOS
UNO = 1 # HAY UN HILILLO TERMIANDO
DOS = 2 # LOS 2 HILILLOS TERMINARON