# -*- coding: utf-8 -*-
"""
    Clase para manejar la logica de cada hilo nucleo
"""
from constantes import *

class HiloDeNucleo():
    
    # Constructor
    def __init__(self, id, tcb, memInst, memDatos, busI, busD):
        self.id = id
        # Matriz que será la cache de instrucciones 
        self.cacheInst =  [[0,0,0,0,-1], 
                           [0,0,0,0,-1],
                           [0,0,0,0,-1],
                           [0,0,0,0,-1]]
        # Matriz que será la cache de datos
        self.cacheDatos = [[0,0,0,0,-1,0], 
                           [0,0,0,0,-1,0],
                           [0,0,0,0,-1,0],
                           [0,0,0,0,-1,0]]
        # Lista para almacenar las instrucciones
        self.memInst = memInst
        # Lista para almacenar los datos
        self.memDatos = memDatos
        # Candado para la memoria de Instrucciones
        self.busInst = busI
        # Candado para la memoria de datos
        self.busDatos = busD
        # Instruction Register
        self.instReg = []
        # Program Counter
        self.progCount = -1
        # Lista con los registros
        self.registros = []
        # TCB
        self.tcb = tcb
        
        
    def run(self):
        self.pruebaLocks()
        
    # Metodo para obtener un hilillo
    def obtenerHilillo(self):
        for hilillo in self.tcb:
            if(hilillo[HILILLO_ESTADO]):
                print("Hilo disponible")
                self.registros = hilillo[HILILLO_REG]
                hilillo[HILILLO_ESTADO] = EJECUCION
            
    # Eliminar
    def pruebaLocks(self):
        # Prueba de locks
        print("Nucleo ",self.id," listo \n")
        if (self.id == 0):
            self.candadoDatos.acquire()
            self.memDatos[0] = 7
            print("\n",self.memDatos,"\n")
            self.candadoDatos.release()
        else:
            self.candadoBusDatos.acquire()
            print("\n",self.memDatos,"\n")
            self.candadoBusDatos.release()
            
