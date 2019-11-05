# -*- coding: utf-8 -*-
"""
    Clase para manejar la logica de cada hilo nucleo
"""
from constantes import *

class HiloDeNucleo():
    
    # Constructor
    def __init__(self, id, tcb, memInst, memDatos, busI, busD, lockTCB):
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
        # Candado de TCB
        self.lockTCB = lockTCB
        
        
    def run(self):
        #self.pruebaLocks()
        hayHilillo = True
        while(hayHilillo == True):
            hayHilillo = self.obtenerHilillo()
            self.imprimirTCB()
        
    # Metodo para obtener un hilillo
    def obtenerHilillo(self):
        self.lockTCB.acquire()
        hayHilillo = False
        for hilillo in self.tcb:
            if(hilillo['estado'] == NO_EJECUTADO):
                hayHilillo = True
                print("Hilo disponible" )
                print(hilillo['id_hilillo'])
                self.registros = hilillo['Registros']
                hilillo['estado'] = EJECUCION
                hilillo['id_nucleo'] = self.id
                self.progCount = hilillo['PC']
                break
        self.lockTCB.release()
        return hayHilillo
                
                
                
    # Eliminar
    def pruebaLocks(self):
        # Prueba de locks
        print("Nucleo ",self.id," listo \n")
        if (self.id == 0):
            self.busDatos.acquire()
            self.memDatos[0] = 7
            print("\n",self.memDatos,"\n")
            self.busDatos.release()
        else:
            self.busDatos.acquire()
            print("\n",self.memDatos,"\n")
            self.busDatos.release()
        
    # Metodo para imprimir la TCB
    def imprimirTCB(self):
        for item in self.tcb:
            print(item)
        
            
