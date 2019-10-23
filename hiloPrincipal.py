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
        self.memDatos = []  # Lista para almacenar los datos
        self.memInst = []   # Lista para almacenar las instrucciones
        self.candadoDatos = threading.Lock() # Candado para la memoria de datos
        self.candadoInst = threading.Lock() # Candado para la memoria de Instrucciones
    
    def run(self):
        # Se llena la memoria de Datos
        self.llenarMenDatos()
        # Se llena la memoria de Instrucciones
        self.llenarMenInst()
        # Se crea el nucleo 0
        nucleo0 = hiloDeNucleo.HiloDeNucleo(0, self.memDatos, self.memInst, self.candadoDatos, self.candadoInst)
        # Se crea el hilo
        nucleo0Thread = threading.Thread(target=nucleo0.run, args=())
        # Se corre el hilo
        nucleo0Thread.start()
        # Se crea el nucleo 1
        nucleo1 = hiloDeNucleo.HiloDeNucleo(1, self.memDatos, self.memInst, self.candadoDatos, self.candadoInst)
        # Se crea el hilo
        nucleo1Thread = threading.Thread(target=nucleo1.run, args=())
        # Se corre el hilo
        nucleo1Thread.start()
        
        print("Si bueno, quien tiene hambre \n")
        
    def llenarMenDatos(self):
        for i in range(0,96):
            self.memDatos.append(i*4)
        print(self.memDatos)
            
    def llenarMenInst(self):
        print("Llenando... jaja")
        