import random
from math import e
import time
import matplotlib.pyplot as plt
import copy

"Diego Duran - Sergio Arriagada"



"""
Para realizar la resolucion de esta instancia, se utilizo una clase que solamnente guarde los tamaños, indices,
y el numero del puesto. Se definio la clase para  realizar el calculo de la funcion objetivo, ya que de esta forma
cuando se realicen los swap no sera necesario cambiar la matriz, al estar los indices (correlativos a la matriz) 
en la clase podremos acceder a los flujos correctos entre los locales
"""
class Local:
    def __init__(self,largoLocal,indice,numeroPuesto):
        self.largoLocal = int(largoLocal)
        self.indice = int(indice)
        self.numeroPuesto = int(numeroPuesto)
""" 
Funcion encargada de leer la opcion para la instancia
"""
def seleccionarInstancia():
    print("Ingrese la instancia que desea resolver:")
    opcion = input("Opcion 1 para 'EjemploProfesora'\nOpcion 2 para 'QAP_sko56_04_n'\nOpcion 3 para 'QAP_sko100_04_n'\nIngrese Opcion: ")
    while(opcion != "1" or opcion != "2" or opcion != "3"):
        if(opcion == "1"):
            return("EjemploProfesora.txt")
        if(opcion == "2"):
            return("QAP_sko56_04_n.txt")
        if(opcion == "3"):
            return("QAP_sko100_04_n.txt")
        opcion = input("Ingrese una opcion valida: ")
    return

""" 
Funcion encargada de leer la instancia previamente seleccionada
"""
def leerInstancia(matriz,vector,nombre):
    archivoInstancia = open(nombre)
    lineaLeer = archivoInstancia.readline().strip().split(",")
    cantidadLocales = int(lineaLeer[0])
    lineaLeer = archivoInstancia.readline().strip().split(",")
    i = 0
    #En este caso se guarda los objetos de tipo Local dentro del vector inicial 
    for x in lineaLeer:
        largoL = int(x)
        index = i 
        nPuesto = i + 1
        localAux = Local(largoL,index,nPuesto)
        i = i + 1
        vector.append(localAux)
    for x in range(0, cantidadLocales):
        lineaLeer = archivoInstancia.readline().strip().split(",")
        for j in range(0, cantidadLocales):
            lineaLeer[j] = int(lineaLeer[j])
        matriz.append(lineaLeer)
    archivoInstancia.close()
    return cantidadLocales

""" 
Funcion encargada de seleccionar la temperatura seleccionada
"""
def seleccionarTemperatura():
    temperatura = float(input("Ingrese Temperatura: "))
    while(temperatura < 0.2):
        temperatura = float(input("Ingrese Temperatura valida: "))
    return temperatura

""" 
Funcion encargada de seleccionar el alpha para ir disminuyendo la temperatura
"""
def seleccionarAlpha():
    alpha = float(input("Ingrese Lambda: "))
    while(alpha <= 0 or alpha >= 1):
        alpha = float(input("Ingrese Lambda entre 0 y 1: "))
    return alpha
""" 
Funcion encargada de aplicar el criterio de metropolis para ver si se acepta una solucion, 
esta retorna true cuando se acepta la solucion
"""
def criterioMetropolis(comparar, temperatura):
    criterio = e**(-comparar/temperatura)
    numeroRandom = random.random()
    if(numeroRandom > criterio):
        return False
    return True
""" 
Funcion encargada de generar un swap 
"""
def generarVecino(vecino,cantidadLocales):
    numeroRandomA = random.randrange(cantidadLocales)
    numeroRandomB = numeroRandomA
    while(numeroRandomB == numeroRandomA):
        numeroRandomB = random.randrange(cantidadLocales)
    aux = vecino[numeroRandomA]
    vecino[numeroRandomA] = vecino[numeroRandomB]
    vecino[numeroRandomB] = aux
    return
""" 
Funcion encargada de calcular la distancia entre los puestos
"""
def calcularDistanciaEntrePuestos(primeraPos, segundaPos, vector):
    distancia = 0.0
    for i in range(primeraPos + 1, segundaPos):
        distancia = distancia + vector[i].largoLocal
    distancia = distancia + ((vector[primeraPos].largoLocal)/2 )+ ((vector[segundaPos].largoLocal)/2)
    return distancia
""" 
Funcion encargada de calcular la funcion objetivo
"""
def calcularFuncionObjetivo(vector,matrizClientes ,cantidadTotalPuestos):
    total = 0.0
    for i in range(cantidadTotalPuestos):
        for j in range(i+1, cantidadTotalPuestos):
            #Se sacan los indices correlativos a la matriz para obtener el flujo correcto entre los locales
            #De esta forma independientemente como se de desordenado el vector de solucion se obtiene siempre el flujo correcto
            indiceI = vector[i].indice
            indiceJ = vector[j].indice
            total = total + (calcularDistanciaEntrePuestos(i,j, vector) * matrizClientes[indiceI][indiceJ])
    return total
""" 
Funcion principal la cual se encarga de aplicar la metaheuristica simulated annealing
"""
def simulatedAnnealing(solucionActual,matriz,nFuncionesObjetivo,funcionesObjetivo,temperatura,alpha,cantidadTotalPuestos,start):
    #Seleccion de la primera solucion, en nuestro caso se busca alazar 5 soluciones, y de esas 3 se usa la mejor para buscasr en en vecindario
    random.shuffle(solucionActual)
    mejorFuncionObjetivo = calcularFuncionObjetivo(solucionActual,matriz,cantidadTotalPuestos)
    solucionAux = []
    mejorFuncionObjetivoAux = 0
    solucionAux = copy.deepcopy(solucionActual)
    for i in range(5):
        random.shuffle(solucionAux)
        mejorFuncionObjetivoAux = calcularFuncionObjetivo(solucionAux,matriz,cantidadTotalPuestos)
        if(mejorFuncionObjetivoAux < mejorFuncionObjetivo):
            solucionActual = copy.deepcopy(solucionAux)
            mejorFuncionObjetivo = mejorFuncionObjetivoAux
    #Se printea la solucion previamente seleccionada 
    print("*****************************************")
    print("Primera Solucion: ")
    print("Funcion Objetivo:", mejorFuncionObjetivo)
    print("Locales:")
    for i in range(cantidadTotalPuestos):
        if(i == cantidadTotalPuestos-1):
            print(solucionActual[i].numeroPuesto)
        else:
            print(solucionActual[i].numeroPuesto,end=",")
    print("\n")
    print("*****************************************")
    #Se guarda la solucion para el grafico
    funcionesObjetivo.append(mejorFuncionObjetivo)
    nFuncionesObjetivo.append(1)
    #Variable x que es usada para contabilizar las soluciones seleccionadas
    x = 2
    #Ciclo principal de la metaheuristica
    while(temperatura > 0.2):
        #Print para ir mostrando la soluciones actuales
        if(x != 2):
            print("Mejor Solucion Actual")
            print("*****************************************")
            print("Funcion Objetivo:", mejorFuncionObjetivo)
            print("Locales:")
            for i in range(cantidadTotalPuestos):
                if(i == cantidadTotalPuestos-1):
                    print(solucionActual[i].numeroPuesto)
                else:
                    print(solucionActual[i].numeroPuesto,end=",")
            print("\n")
            print("*****************************************")
        #Se genera una copia de la solucion para buscar en un vecino
        vecino = copy.deepcopy(solucionActual)
        generarVecino(vecino,cantidadTotalPuestos)
        funcionObjetivoVecino = calcularFuncionObjetivo(vecino,matriz,cantidadTotalPuestos)
        #Si la solucion del vecino generado atravez de swap es mejor directamente se acepta y se reenplaza por la solucion actual
        if(funcionObjetivoVecino < mejorFuncionObjetivo):
            funcionesObjetivo.append(mejorFuncionObjetivo)
            nFuncionesObjetivo.append(x)
            mejorFuncionObjetivo = funcionObjetivoVecino
            solucionActual = copy.deepcopy(vecino)
        #Sino se pasa a evaluar el criterio de metropolis
        else:
            aceptarVecino = criterioMetropolis((funcionObjetivoVecino - mejorFuncionObjetivo), temperatura)
            if(aceptarVecino == True):
                funcionesObjetivo.append(mejorFuncionObjetivo)
                nFuncionesObjetivo.append(x)
                mejorFuncionObjetivo = funcionObjetivoVecino
                solucionActual = copy.deepcopy(vecino)
                
        # Se disminuye la temperatura
        temperatura = temperatura*alpha
        x += 1


    # Se termina el contador de tiempo
    #end = time.time()
    end = time.time()
    #Se printea la mejor solucion
    print("*****************************************")
    print("Mejor Solucion encontrada:")
    print("Funcion objetivo", mejorFuncionObjetivo)
    print("Locales:")
    for i in range(cantidadTotalPuestos):
        if(i == cantidadTotalPuestos-1):
            print(solucionActual[i].numeroPuesto)
        else:
            print(solucionActual[i].numeroPuesto,end=",")     
    print("\n")
    print("*****************************************")
    print("Tiempo De Ejecucion:", end-start, "Segundos")
    print("Cantida de iteraciones:",x)
    # Creacion del grafico para ver el comportamiento
    plt.plot(nFuncionesObjetivo, funcionesObjetivo, "-ok")
    plt.xlabel("Numero De Intento")
    plt.ylabel("Funcion Objetivo")
    plt.show()

""" 
MAIN
vectorIncial: es el vector inicial el cual se guarda la los posicion incial de los locales, su tamaño, y numero del puesto
matrizFlujo: es la matriz que guarda los flujos de los clientes 
nFuncionesObjetivo: es el vector que guarda la cantidad de soluciones aceptadas
funcionesObjetivo: es el vector que guarda las funciones objtevios aceptadas
nombreInstancia: es la variable que guarda el nombre de la instancia para ejecutar
totalPuestos: es la variable que guarda la cantidad de puestos
temperatura: es la variable que guarda la temperatura inical para la metaheuristica
alpha: es la variable que guarda el alpha para el enfriamiento geotermirco
start: es la variable de tipo time para contar los segundos de la ejecucion
"""
vectorIncial = []
matrizFlujo = []
nFuncionesObjetivo = []
funcionesObjetivo = []
nombreInstancia = seleccionarInstancia()
totalPuestos =  leerInstancia(matrizFlujo,vectorIncial,nombreInstancia)
temperatura = seleccionarTemperatura()
alpha = seleccionarAlpha()
start = time.time()
simulatedAnnealing(vectorIncial,matrizFlujo,nFuncionesObjetivo,funcionesObjetivo,temperatura,alpha,totalPuestos,start)
