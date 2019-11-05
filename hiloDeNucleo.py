# -*- coding: utf-8 -*-
"""
    Clase para manejar la logica de cada hilo nucleo
"""
from constantes import *

class HiloDeNucleo():
    
    # Constructor
    def __init__(self, id, tcb, memInst, memDatos, busI, busD, lockTCB, barrera, miCacheLock, otraCacheLock, miCache,
                 otraCache):
        self.id = id
        # Matriz que será la cache de instrucciones 
        self.cacheInst =  [[0,0,0,0,-1], 
                           [0,0,0,0,-1],
                           [0,0,0,0,-1],
                           [0,0,0,0,-1]]
        # Matriz que será la cache de datos
        self.miCacheDatos = miCache
        # Cache del otro Nucleo
        self.otraCache = otraCache
        
        # Ciclo de reloj
        self.cicloReloj = 0
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
        # Barrera de ciclo reloj
        self.barrera = barrera
        # Candado para mi cache
        self.miCacheLock = miCacheLock
        # Candado para la otra cache
        self.otraCacheLock = otraCacheLock
        
        
        
    def run(self):
        #self.pruebaLocks()
        hayHilillo = True
        while(hayHilillo == True):
            terminarHilillo = False
            hayHilillo = self.obtenerHilillo()
            while(terminarHilillo == False):
                numBloque = self.progCount / 16
                if(estaEnCache(numBloque) == False):
                    self.cargarBloqueInst(numBloque)
                    
                self.instReg = self.cacheInst[(numBloque % 4)][(self.progCount % 16)/4]    
                self.progCount+=4 # Observar si esto sirve para el branch
                # Identificacion del  
                if(self.instReg[0] == 999):
                    terminarHilillo = True
                elif(self.instReg[0] == 37):
                    self.funcStore()
                
                numBloque -= 24
            self.imprimirTCB()
            
    # Metodo que se encarga de realizar el Store Word 
    def funcStore(self): 
        self.miCacheLock.acquire()
        
        dirMemDatos = self.registros[self.instReg[1]] + self.instReg[3] 
        numBloque = dirMemDatos / 16
        self.busDatos.acquire()
        
        self.otraCacheLock.acquire()
        
        # Se invalida la otra cache o no
        if(numBloque == self.otraCache[(numBloque % 4)][ID_BLOQUE]):
            self.otraCache[(numBloque % 4)][5] = INVALIDO
        
        
        self.otraCacheLock.release()
        
        # GUARDAR EN LA MEMORIA DE DATOS - (la palabra, no el bloque)
        # PASAR LOS CICLOS DE RELOJ
        
        self.busDatos.release()
        
        # SI EL BLOQUE ESTA EN MI CACHE, SE ESCRIBE ALLÍ, SINO NO
            
        self.miCacheLock.release()
            
        
    # Metodo para cargar bloque de memoria de instrucciones a cache de instrucciones
    def cargarBloqueInst(self, numBloque):
        self.busInst.acquire()
        bloqueEnMemInst = numBloque - 24
        for i in range(0, 4):
            self.cacheInst[numBloque % 4][i][0] = self.memInst[bloqueEnMemInst]
            self.cacheInst[numBloque % 4][i][1] = self.memInst[bloqueEnMemInst+1]
            self.cacheInst[numBloque % 4][i][2] = self.memInst[bloqueEnMemInst+2]
            self.cacheInst[numBloque % 4][i][3] = self.memInst[bloqueEnMemInst+3]
            bloqueEnMemInst += 4
        self.cacheInst[(numBloque % 4)][ID_BLOQUE] = numBloque
        # Pasar los ciclos de reloj
        for i in range(0,10):
            self.barrera.wait()
            self.cicloReloj+=1
        self.busInst.release()
        
        
        
    # Metodo para saber si un bloque esta en caché de Inst
    def estaEnCache(self, numBloque):
        if(numBloque == self.cacheInst[(numBloque % 4)][ID_BLOQUE]):
            return True
        return False
            

    
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
        
            
