# -*- coding: utf-8 -*-
"""
    Clase para manejar la logica de cada hilo nucleo
"""

class HiloDeNucleo():
    
    # Constructor
    def __init__(self, id, memDatos, memInst, candadoD, candadoI):
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
        self.candadoInst = candadoI
        # Candado para la memoria de datos
        self.candadoDatos = candadoD
        
        
    def run(self):
        self.pruebaLocks()
            
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
            self.candadoDatos.acquire()
            print("\n",self.memDatos,"\n")
            self.candadoDatos.release()
            
