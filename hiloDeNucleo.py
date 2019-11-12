# -*- coding: utf-8 -*-
"""
    Clase para manejar la logica de cada hilo nucleo
"""
import constantes as c

class HiloDeNucleo():
    
    # Constructor
    def __init__(self, id, tcb, memInst, memDatos, busI, busD, lockTCB, barrera, miCacheLock, otraCacheLock, miCache,
                 otraCache, candadoEscritura, hF):
        # Identificacion del nucleo 
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
        
        # ---- Candados ----
        
        # Candado de TCB
        self.lockTCB = lockTCB
        # Candado para mi cache
        self.miCacheLock = miCacheLock
        # Candado para la otra cache
        self.otraCacheLock = otraCacheLock
        # Candado para escribir en consola
        self.candadoEscritura = candadoEscritura
        # Barrera de ciclo reloj
        self.barrera = barrera
        # Variable para saber cuantos hilos han terminado su ejecución
        self.hilillosFinalizados = hF
        
        
    def run(self):
        # Variable para saber si hay hilillos por ejecutar en la TCB
        hayHilillo = True 
        while(hayHilillo == True):
            # Obtenemos el hilillo
            hayHilillo = self.obtenerHilillo()
            if(hayHilillo):
                # Ejecutamos la instruccion
                self.ejecutarInst()
                
        self.candadoEscritura.acquire()
        if(self.hilillosFinalizados[0] == c.NINGUNO):
            self.hilillosFinalizados[0] = c.UNO
            self.candadoEscritura.release()
            fin = False
            while(fin == False):
                self.candadoEscritura.acquire()
                if(self.hilillosFinalizados[0] == c.DOS):
                    fin = True
                self.candadoEscritura.release()
                if(fin == False):
                    self.pasarCicloReloj(1)
        elif(self.hilillosFinalizados[0] == c.UNO):
            self.hilillosFinalizados[0] = c.DOS
            self.candadoEscritura.release()
            self.imprimirTCB()
            print("Mem Datos: \n", self.memDatos)
            
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
            self.progCount += 4 
            # Obtenemos la instruccion
            instruccion = self.instReg[0]
            # Identificacion de la instruccion
            if(instruccion == 999):
                self.terminarHilillo()
                terminarHilillo = True
            elif(instruccion == 5):
                # Es un Load
                self.imprimir("Inst Load")
                self.load()
                self.imprimir("Salio del Load")
            elif(instruccion == 19):
                # Es un Addi
                self.imprimir("Inst Addi")
                self.addi()
                self.imprimir("Salio del Addi")
            elif(instruccion == 37):
                # Es un Store
                self.imprimir("Inst Store")
                self.store()
                self.imprimir("Salio del store")
            elif(instruccion == 56):
                # Es un Load
                self.imprimir("Inst Div")
                self.div()
                self.imprimir("Salio del div")
            elif(instruccion == 71):
                # Es un Load
                self.imprimir("Inst Add")
                self.add()
                self.imprimir("Salio del Add")
            elif(instruccion == 72):
                # Es un Load
                self.imprimir("Inst Mul")
                self.mul()
                self.imprimir("Salio del mul")
            elif(instruccion == 83):
                # Es un Sub
                self.imprimir("Inst Sub")
                self.sub()
                self.imprimir("Salio del sub")
            elif(instruccion == 99):
                # Es un Beq
                self.imprimir("Inst Beq")
                self.beq()
                self.imprimir("Salio del beq")
            elif(instruccion == 100):
                # Es un Bne
                self.imprimir("Inst Bne")
                self.bne()
                self.imprimir("Salio del Bne")
            elif(instruccion == 103):
                # Es un Jar
                self.imprimir("Inst Jalr")
                self.jalr()
                self.imprimir("Salio del jalr")
            elif(instruccion == 111):
                # Es un Jalr
                self.imprimir("Inst Jal")
                self.jal()
                self.imprimir("Salio del jal")
            self.pasarCicloReloj(1)
    
    # Metodo que realiza el Addi
    def addi(self):
        suma = self.registros[self.instReg[2]] + self.instReg[3]
        self.registros[self.instReg[1]] = suma
        
    
    # Metodo que realiza el Add
    def add(self):
        suma = self.registros[self.instReg[2]] + self.registros[self.instReg[3]]
        self.registros[self.instReg[1]] = suma
        
    # Metodo que se encarga de hacer el sub
    def sub(self):
        resta = self.registros[self.instReg[2]] - self.registros[self.instReg[3]]
        self.registros[self.instReg[1]] = resta
        
     # Metodo que se encarga de hacer el mul
    def mul(self):
        multiplicacion = self.registros[self.instReg[2]] * self.registros[self.instReg[3]]
        self.registros[self.instReg[1]] = int(multiplicacion)
        
     # Metodo que se encarga de hacer el div
    def div(self):
        division = (self.registros[self.instReg[2]] / self.registros[self.instReg[3]])
        self.registros[self.instReg[1]] = int(division)
        
    # Metodo que se encarga de hacer el branch equal
    def beq(self):
        if(self.registros[self.instReg[1]] == self.registros[self.instReg[2]]):
            self.progCount += (self.instReg[3] * 4)
                
            
    # Metodo que se encarga de hacer el branch not equal
    def bne(self):
        if(self.registros[self.instReg[1]] != self.registros[self.instReg[2]]):
            self.progCount += (self.instReg[3] * 4)
            
    # Metodo que hace el jal
    def jal(self):
        self.registros[self.instReg[1]] = self.progCount
        self.progCount += self.instReg[3]
           
    # Metodo que hace el jalr
    def jalr(self):
        self.registros[self.instReg[1]] = self.progCount
        self.progCount = self.registros[self.instReg[2]] + self.instReg[3]
            
    # Metodo que se encarga de realizar el Store Word 
    def store(self):
        obtenerMiCache = False
        # Se obtiene la direccion en la memoria de datos en la cual se almacenará el valor
        dirMemDatos = self.registros[self.instReg[1]] + self.instReg[3] 
        # Se busca obtiene el numero de bloque
        numBloque = int(dirMemDatos / 16)
        # Se busca la palabra
        indicePalabra = int((dirMemDatos % 16) / 4)
        # Se obtiene el indice del bloque en la cache
        indiceBloque = int(numBloque % 4)
        # Direccion final en memoria de datos
        dirFinal = int(dirMemDatos/4)
        while(obtenerMiCache == False):
            # Se pide el candado
            obtenerMiCache = self.miCacheLock.acquire(False)
            # Si se obtiene
            if (obtenerMiCache):
                # Se pide el bus de datos
                obtenerBusDatos = self.busDatos.acquire(False)
                # Si se obtiene
                if(obtenerBusDatos):
                    # Se aumenta el ciclo de reloj
                    self.pasarCicloReloj(1, True)
                    obtenerOtraCache = False
                    while(obtenerOtraCache == False):
                        # Se pide la otra cache
                        obtenerOtraCache = self.otraCacheLock.acquire(False)
                        # Si se obtiene
                        if(obtenerOtraCache):
                            # Se aumenta el ciclo de reloj
                            self.pasarCicloReloj(1, True)
                            # Se verifica si el bloque esta en la otra cache
                            if(numBloque == self.otraCache[indiceBloque][c.ID_BLOQUE]):
                                # Se invalida la otra cache
                                self.otraCache[indiceBloque][c.ESTADO_BLOQUE] = c.INVALIDO
                                # Se pasa 1 ciclo de reloj 
                                self.pasarCicloReloj(1, True)
                            # Se libera el candado de la otra cache
                            self.otraCacheLock.release()
                        # Si no se obtiene la otra cache
                        else:
                            # Se pasa 1 ciclo de reloj
                            self.pasarCicloReloj(1)
                            
                        
                    # GUARDAR EN LA MEMORIA DE DATOS - (la palabra, no el bloque)
                    self.memDatos[dirFinal] = self.registros[self.instReg[2]]
                    
                    # SI EL BLOQUE ESTA EN MI CACHE, SE ESCRIBE ALLÍ, SINO NO
                    if(self.estaEnCacheDatos(numBloque)):
                        self.miCacheDatos[indiceBloque][indicePalabra] = self.registros[self.instReg[2]]
                    
                    # Pasar los ciclos de reloj
                    self.pasarCicloReloj(5, True)
                    
                    # Se libera el candado
                    self.busDatos.release()
                        
                # Si no se obtiene el bus de datos
                else:
                    obtenerMiCache = False
                    # Se pasa 1 ciclo de reloj
                    self.pasarCicloReloj(1, True)
                    
                # Se libera el candado
                self.miCacheLock.release()
                
                self.pasarCicloReloj(1)
                
            # Si no se obtiene mi cache
            else:
                # Se pasa 1 ciclo de reloj
                self.pasarCicloReloj(1, True)

    def load(self):
        obtenerMiCache = False
        # Se obtiene la direccion en la memoria de datos en la cual se almacenará el valor
        dirMemDatos = self.registros[self.instReg[2]] + self.instReg[3] 
        # Se busca obtiene el numero de bloque
        numBloque = int(dirMemDatos / 16)
        # Se busca la palabra en la cache
        indicePalabra = int((dirMemDatos % 16) / 4)
        # Se obtiene el indice del bloque en la cache
        indiceBloque = int(numBloque % 4)
        # Obtenemos el registro
        reg = self.instReg[1]
        while(obtenerMiCache == False):
            # Se pide el candado
            obtenerMiCache = self.miCacheLock.acquire(False)
            # Si se obtiene
            if (obtenerMiCache):
                # Se verifica si no esta en la cache el bloque
                if(self.estaEnCacheDatos(numBloque)):
                    # Se pasa la palabra de la cache de datos al registro correspondiente
                    self.registros[reg] = self.miCacheDatos[indiceBloque][indicePalabra]
                # Si no esta en la cache
                else:
                    # Se pide el bus de datos
                    obtenerBusDatos = self.busDatos.acquire(False)
                    # Si se obtiene
                    if(obtenerBusDatos):
                        # Se aumenta el ciclo de reloj
                        self.pasarCicloReloj(1)
                        
                        # Subir el bloque
                        self.cargarBloqueDatos(numBloque, indiceBloque)
                        
                        # Se valida el bloque en la cache de datos
                        self.miCacheDatos[indiceBloque][c.ESTADO_BLOQUE] = c.VALIDO
                        
                         # Se pasa la palabra de la cache de datos al registro correspondiente
                        self.registros[reg] = self.miCacheDatos[indiceBloque][indicePalabra]
                        
                        # Pasar los ciclos de reloj
                        self.pasarCicloReloj(20)
                        
                        # Se libera el candado
                        self.busDatos.release()
                            
                    # Si no se obtiene
                    else:
                        # Se pasa 1 ciclo de reloj
                        self.pasarCicloReloj(1)
                        obtenerMiCache = False
                    
                # Se libera el candado
                self.miCacheLock.release()
                self.pasarCicloReloj(1)
                                
            # Si no se obtiene
            else:
                # Se pasa 1 ciclo de reloj
                self.pasarCicloReloj(1)
                
                
    #Metodo para cargar bloque de memoria de datos a cache de datos
    def cargarBloqueDatos(self, numBloque, indiceBloque):
        bloqueEnMemDatos = numBloque*4
        for i in range(0,4):
            self.miCacheDatos[indiceBloque][i] = self.memDatos[bloqueEnMemDatos+i]
            
        
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
                    try:
                        # palabra 0
                        self.cacheInst[indiceBloque][i][0] = self.memInst[bloqueEnMemInst]
                        # palabra 1
                        self.cacheInst[indiceBloque][i][1] = self.memInst[bloqueEnMemInst+1]
                        # palabra 2
                        self.cacheInst[indiceBloque][i][2] = self.memInst[bloqueEnMemInst+2]
                        # palabra 3
                        self.cacheInst[indiceBloque][i][3] = self.memInst[bloqueEnMemInst+3]
                    except IndexError:
                         # palabra 0
                        self.cacheInst[indiceBloque][i][0] = 0
                        # palabra 1
                        self.cacheInst[indiceBloque][i][1] = 0
                        # palabra 2
                        self.cacheInst[indiceBloque][i][2] = 0
                        # palabra 3
                        self.cacheInst[indiceBloque][i][3] = 0
                    bloqueEnMemInst += 4
                # Se le agrega el numero de bloque que se cargo a la cache
                self.cacheInst[indiceBloque][c.ID_BLOQUE] = numBloque
                # Pasar los ciclos de reloj
                self.pasarCicloReloj(10)
                self.busInst.release()
            # Si no se obtiene
            else:
                self.pasarCicloReloj(1)
        
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
        if(numBloque == self.miCacheDatos[indiceBloque][c.ID_BLOQUE] and self.miCacheDatos[indiceBloque][c.ESTADO_BLOQUE] == c.VALIDO):
            return True
        return False
    
    # Metodo para obtener un hilillo del TCB
    def obtenerHilillo(self):
        # Se bloquea la TCB
        self.lockTCB.acquire()
        hayHilillo = False
        # Se busca sobre la lista de hilillos
        for hilillo in self.tcb:
            # Si existe un hilillo que no ha sido ejecitado
            if(hilillo['estado'] == c.NO_EJECUTADO):
                hayHilillo = True
                self.imprimir("************************************ Hilillo disponible id: "+str(hilillo['id_hilillo']))
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
    
    
    # Metodo que guarda valor de los registros del nucleo a la tbc y el estado lo pasa a terminado
    def terminarHilillo(self):
        # Se bloquea la TCB
        self.lockTCB.acquire()
        for hilillo in self.tcb:
            if(hilillo['estado'] == c.EJECUCION and hilillo['id_nucleo'] == self.id):
                self.imprimir("++++++++++++++++++++++ Hilillo terminado id: "+str(hilillo['id_hilillo']))
                # Se cargan los registros del nucleo a la TCB
                hilillo['Registros'] = self.registros
                # Se pone el estado en Ejecucion
                hilillo['estado'] = c.TERMINADO
                break
        # Se bloquea la TCB
        self.lockTCB.release()
            
    # Metodo para pasar ciclos de reloj
    def pasarCicloReloj(self, n, b = False):
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
        print("Nucleo: ", self.id, ", ", msj)
        # Se libera el candado
        self.candadoEscritura.release()
    
     # Metodo para imprimir la TCB
    def imprimirTCB(self):
        print("----  Resultados  ----")
        print("** TCB **\n\n")
        for item in self.tcb:
            print("EL HILILLO ", item['id_hilillo'])
            print(item)
            contador = 0
            for item2 in item['Registros']:
                print("x"+ str(contador) + ": ", item2)
                contador+=1
            print("\n\n\n")
        

            
