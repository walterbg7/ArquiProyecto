# -*- coding: utf-8 -*-
"""
    Clase para manejar la logica de cada hilo nucleo
"""
#from constantes import *
import constantes as c

class HiloDeNucleo():
    
    # Constructor
    def __init__(self, id, tcb, memInst, memDatos, busI, busD, lockTCB, barrera, miCacheLock, otraCacheLock, miCache,
                 otraCache, candadoEscritura):
        self.id = id
        # Matriz que será la cache de instrucciones
        self.cacheInst =  [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],-1], 
                           [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],-1],
                           [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],-1],
                           [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],-1]]
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
        # Candado para escribir en consola
        self.candadoEscritura = candadoEscritura
        
        
        
    def run(self):
        #self.pruebaLocks()
        hayHilillo = True
        while(hayHilillo == True):
            # Obtenemos el hilillo
            hayHilillo = self.obtenerHilillo()
            # Ejecutamos la intruccion
            self.ejecutarInst()
            
    def ejecutarInst(self):
        terminarHilillo = False
        while(terminarHilillo == False):
            # Se obtiene el numero de bloque
            numBloque = int(self.progCount / 16)
            # Se pregunta si el bloque está en la cache de instrucciones
            if(self.estaEnCacheInst(numBloque) == False):
                # Si no esta se carga el bloque
                self.cargarBloqueInst(numBloque)
            # Se obtine el indice del bloque en cache
            indiceBloque = int(numBloque % 4)
            # Se obtiene la palabra del bloque
            indicePalabra = int((self.progCount % 16)/4)
            # Se carga la instruccion al intruction register
            self.instReg = self.cacheInst[indiceBloque][indicePalabra]
            self.imprimir("IR: "+str(self.instReg))
            # Se aumenta el program counter
            self.progCount += 4 # ------ Observar si esto sirve para el branch -----
            # Obtenemos la instruccion
            intruccion = self.instReg[0]
            # Identificacion de la instruccion
            if(intruccion == 999):
                terminarHilillo = True
            elif(intruccion == 5):
                # Es un Load
                self.imprimir("Inst Load")
            elif(intruccion == 19):
                # Es un Addi
                self.imprimir("Inst Addi")
            elif(intruccion == 37):
                # Es un Store
                self.imprimir("Inst Store")
                #self.funcStore()
            elif(intruccion == 56):
                # Es un Load
                self.imprimir("Inst Load")
            elif(intruccion == 71):
                # Es un Load
                self.imprimir("Inst Load")
            elif(intruccion == 72):
                # Es un Load
                self.imprimir("Inst Load")
            elif(intruccion == 83):
                # Es un Sub
                self.imprimir("Inst Sub")
            elif(intruccion == 99):
                # Es un Beq
                self.imprimir("Inst Beq")
            elif(intruccion == 100):
                # Es un Bne
                self.imprimir("Inst Bne")
            elif(intruccion == 103):
                # Es un Jar
                self.imprimir("Inst Jar")
            elif(intruccion == 111):
                # Es un Jalr
                self.imprimir("Inst Jalr")
            
    # Metodo que se encarga de realizar el Store Word 
    def funcStore(self):
        obtenerMiCache = False
        while(obtenerMiCache == False):
            # Se pide el candado
            obtenerMiCache = self.miCacheLock.acquire(False)
            # Si se obtiene
            if (obtenerMiCache):
                # Se obtiene la direccion en la memoria de datos en la cual se almacenará el valor
                dirMemDatos = self.registros[self.instReg[1]] + self.instReg[3] 
                # Se busca obtiene el numero de bloque
                numBloque = int(dirMemDatos / 16)
                # Se busca la palabra
                numPalabra = int((dirMemDatos % 16) / 4)
                # Se obtiene el indice del bloque en la cache
                indiceBloque = int(numBloque % 4)
                # Se pide el bus de datos
                obtenerBusDatos = self.busDatos.acquire()
                # Si se obtiene
                if(obtenerBusDatos):
                    # Se aumenta el ciclo de reloj
                    self.pasarCicloReloj(1)
                    obtenerOtraCache = False
                    while(obtenerOtraCache == False):
                        # Se pide la otra cache
                        obtenerOtraCache = self.otraCacheLock.acquire()
                        # Si se obtiene
                        if(obtenerOtraCache):
                            # Se aumenta el ciclo de reloj
                            self.pasarCicloReloj(1)
                            # Se verifica si el bloque esta en la otra cache
                            if(numBloque == self.otraCache[indiceBloque][c.ID_BLOQUE]):
                                # Se invalida la otra cache
                                self.otraCache[indiceBloque][5] = c.INVALIDO
                            # Se libera el candado de la otra cache
                            self.otraCacheLock.release()
                        # Si no se obtiene la otra cache
                        else:
                            # Se pasa 1 ciclo de reloj
                            self.pasarCicloReloj(1)
                        
                    # GUARDAR EN LA MEMORIA DE DATOS - (la palabra, no el bloque)
                    #self.memDatos[]
                    
                    # SI EL BLOQUE ESTA EN MI CACHE, SE ESCRIBE ALLÍ, SINO NO
                    #if(self.estaEnCacheDatos(numBloque)):
                    
                    # Pasar los ciclos de reloj
                    self.pasarCicloReloj(5)
                    
                    # Se libera el candado
                    self.busDatos.release()
                        
                # Si no se obtiene el bus de datos
                else:
                    obtenerMiCache = False
                    # Se pasa 1 ciclo de reloj
                    self.pasarCicloReloj(1)
                    
                # Se libera el candado
                self.miCacheLock.release()
                
            # Si no se obtiene mi cache
            else:
                # Se pasa 1 ciclo de reloj
                self.pasarCicloReloj(1)

    def load(self):
        obtenerMiCache = False
        while(obtenerMiCache == False):
            # Se pide el candado
            obtenerMiCache = self.miCacheLock.acquire(False)
            # Si se obtiene
            if (obtenerMiCache):
                # Se obtiene la direccion en la memoria de datos en la cual se almacenará el valor
                dirMemDatos = self.registros[self.instReg[2]] + self.instReg[3] 
                # Se busca obtiene el numero de bloque
                numBloque = int(dirMemDatos / 16)
                # Se busca la palabra
                numPalabra = int((dirMemDatos % 16) / 4)
                # Se obtiene el indice del bloque en la cache
                indiceBloque = int(numBloque % 4)
                # Obtenemos el registro
                reg = self.instReg[1]
                # Se verifica si no esta en la cache el bloque
                if(self.estaEnCacheDatos()):
                    self.registros[reg] = self.miCacheDatos[indiceBloque][numPalabra]
                # Si no esta en la cache
                else:
                    # Se pide el bus de datos
                    obtenerBusDatos = self.busDatos.acquire()
                    # Si se obtiene
                    if(obtenerBusDatos):
                        # Se aumenta el ciclo de reloj
                        self.pasarCicloReloj(1)
                        
                        # Subir el bloque
                        
                        
                        # Pasar los ciclos de reloj
                        self.pasarCicloReloj(5)
                        
                        # Se libera el candado
                        self.busDatos.release()
                            
                    # Si no se obtiene
                    else:
                        # Se pasa 1 ciclo de reloj
                        self.pasarCicloReloj(1)
                    
                # Se libera el candado
                self.miCacheLock.release()
                
            # Si no se obtiene
            else:
                # Se pasa 1 ciclo de reloj
                self.pasarCicloReloj(1)
            
        
    # Metodo para cargar bloque de memoria de instrucciones a cache de instrucciones
    def cargarBloqueInst(self, numBloque):
        obtenerBus = False
        # Se obtiene el indice del bloque en la cache
        indiceBloque = int(numBloque % 4)
        while(obtenerBus == False):
            # Se pide el bus de Instrucciones
            obtenerBus = self.busInst.acquire(False)
            # Si se obtiene
            if(obtenerBus):
                # Se obtiene la direcccion del bloque en la memoria de instrucciones
                bloqueEnMemInst = (numBloque - 24)*16
                # Se cargan las 4 palabras en la cache
                for i in range(0, 4):
                    # palabra 0
                    self.cacheInst[indiceBloque][i][0] = self.memInst[bloqueEnMemInst]
                    # palabra 1
                    self.cacheInst[indiceBloque][i][1] = self.memInst[bloqueEnMemInst+1]
                    # palabra 2
                    self.cacheInst[indiceBloque][i][2] = self.memInst[bloqueEnMemInst+2]
                    # palabra 3
                    self.cacheInst[indiceBloque][i][3] = self.memInst[bloqueEnMemInst+3]
                    bloqueEnMemInst += 4
                # Se le agrega el numero de bloque que se cargo a la cache
                self.cacheInst[indiceBloque][c.ID_BLOQUE] = numBloque
                # Pasar los ciclos de reloj
                self.pasarCicloReloj(10)
                self.busInst.release()
            # Si no se obtiene
            else:
                self.pasarCicloReloj(1)
        self.imprimirCI()
        
    # Metodo para saber si un bloque esta en caché de Inst
    def estaEnCacheInst(self, numBloque):
        # Se pregunta si el bloque está en la cache
        indiceBloque = int(numBloque % 4)
        if(numBloque == self.cacheInst[indiceBloque][c.ID_BLOQUE]):
            return True
        return False
    
    # Metodo para saber si un bloque esta en caché de Datos
    def estaEnCacheDatos(self, numBloque):
        # Se pregunta si el bloque está en la cache
        indiceBloque = int(numBloque % 4)
        if(numBloque == self.miCacheDatos[indiceBloque][c.ID_BLOQUE]):
            return True
        return False
    
    # Metodo para obtener un hilillo
    def obtenerHilillo(self):
        # Se bloquea la TCB
        self.lockTCB.acquire()
        hayHilillo = False
        # Se busca sobre la lista de hilillos
        for hilillo in self.tcb:
            # Si existe un hilillo que no ha sido ejecitado
            if(hilillo['estado'] == c.NO_EJECUTADO):
                hayHilillo = True
                self.imprimir("Hilillo disponible id: "+str(hilillo['id_hilillo']))
                # Se cargan los registros de la TCB a los registros del nucleo
                self.registros = hilillo['Registros']
                # Se pone el estado en Ejecucion
                hilillo['estado'] = c.EJECUCION
                # Se le indica el id del nucleo que ejecutará el hilillo
                hilillo['id_nucleo'] = self.id
                # Se le asigna valor al Program Counter
                self.progCount = hilillo['PC']
                break
        # Se libera el candado
        self.lockTCB.release()
        # Se retorna true si hay algun hilillo que ejecutar, en caso contrario False
        return hayHilillo
            
    # Metodo para pasar ciclos de reloj
    def pasarCicloReloj(self, n):
        # Se hace un for por la cantidad de ciclos de reloj que se quieren pasar
        for i in range(0, n):
            # Se espera en la barrera al otro nucleo 
            self.barrera.wait()
            # Se aumenta el ciclo de reloj
            self.cicloReloj += 1
            
    # Metodo para imprimir en consola
    def imprimir(self, msj):
        # Se obtiene candado
        self.candadoEscritura.acquire()
        # Se imprime el mensaje
        print(msj)
        # Se libera el candado
        self.candadoEscritura.release()
        
    # Metodo para imprimir la TCB
    def imprimirTCB(self):
        self.imprimir("***TCB***")
        for item in self.tcb:
            self.imprimir(item)
    
    # Metodo para imprimir la Cache de Instruciones
    def imprimirCI(self):
        self.imprimir("Cache de Instrcciones")
        for item in self.cacheInst:
            self.imprimir(item)
    
    # Metodo para imprimir la Cache de Datos
    def imprimirCD(self):
        self.imprimir("Cache de Datos")
        for item in self.miCacheDatos:
            self.imprimir(item)
        
            
