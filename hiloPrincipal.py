# -*- coding: utf-8 -*-
"""
    Clase para manejar la logica del hilo principal
"""
import threading
import hiloDeNucleo

class HiloPrincipal():
    
    # Constructor
    def __init__(self):
        self.tcb = [] # Tabla de contextos
        self.memInst = []   # Lista para almacenar las instrucciones
        self.memDatos = []  # Lista para almacenar los datos
        self.candadoBusInst = threading.Lock() # Candado para aceso a la memoria de Instrucciones
        self.candadoBusDatos = threading.Lock() # Candado para aceso a la memoria de datos
    
    def run(self):
        # Se llena la memoria de Datos
        self.llenarMenDatos()
        # Se llena la memoria de Instrucciones
        self.llenarMenInst()
        # Se crea el nucleo 0
        nucleo0 = hiloDeNucleo.HiloDeNucleo(0, self.tcb, self.memInst, self.memDatos, self.candadoBusInst, self.candadoBusDatos)
        # Se crea el hilo
        nucleo0Thread = threading.Thread(target=nucleo0.run, args=())
        # Se corre el hilo
        nucleo0Thread.start()
        # Se crea el nucleo 1
        nucleo1 = hiloDeNucleo.HiloDeNucleo(1, self.tcb, self.memInst, self.memDatos, self.candadoBusInst, self.candadoBusDatos)
        # Se crea el hilo
        nucleo1Thread = threading.Thread(target=nucleo1.run, args=())
        # Se corre el hilo
        nucleo1Thread.start()
        
        print("Si bueno, quien tiene hambre \n")
        
    def llenarMenDatos(self):
        for i in range(0,96):
            self.memDatos.append(i*4)
        print(self.memDatos)
            
    
    def llenarTCB(self, pc, nombre_archivo):
        registros = []
        for i in range(0,31):
            registros.append(0)
        diccionario = {'PC':pc,'Registros:':registros, 'id_nucleo':-1, 
        'id_hilillo':nombre_archivo, 'estado':0}
        self.tcb.append(diccionario)
    
    def llenarMenInst(self):
        print("Llenando... jaja")
        indiceMemInst = 383
        for arch in range(0,7):
            nombre_archivo = str(arch) + ".txt"
            f = open(nombre_archivo, 'r')
            contenido = f.read()
            print(contenido)
            instrucciones = contenido.split("\n")
            #contadorInst = 1
            ponerEnTCB = False
            for instruccion in instrucciones:
                entero = instruccion.split(" ")
                for i in entero:
                    try:
                        self.memInst.append(int(i))
                        indiceMemInst += 1
                        if(ponerEnTCB == False): # Para solo meter la primera instruccion de cada hilillo
                            self.llenarTCB(indiceMemInst, arch)
                            ponerEnTCB = True
                    except ValueError:
                        pass
            f.close()
        print(self.memInst)
        print(self.tcb)