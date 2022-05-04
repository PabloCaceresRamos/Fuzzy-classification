import random




def generarPoblacion(numeroPoblacion,BR):

    poblacion=[None]*numeroPoblacion
    poblacion[0]=[1]*len(BR)#El primero tendra todas las reglas activadas

    for i in range(1,numeroPoblacion):#Creamos el resto de la población rellenando aleatoriamente entre 1 y 0
        poblacion[i]=[None]*len(BR)
        for j in range(len(BR)):
            poblacion[i][j]=random.randrange(0,2,1)

    return poblacion

def calcularH(x1,x2,x3,ve):
    #fig, ax = plt.subplots()
    #ax.plot([x1,x2,x3],[0,1,0])
    
    if ve<x1: 
        #ax.scatter([ve],[0],color = "tab:red")
        return 0
    if(ve>x3): 
        #ax.scatter([ve],[0],color = "tab:red")
        return 0
    if(ve==x2): 
       # ax.scatter([ve],[0])
        return 1
    if ve<x2: 
       # ax.scatter([ve],[0],color = "tab:orange")
        return (ve-x1)/(x2-x1)
    else: 
        #ax.scatter([ve],[0],color = "tab:gray")
        return (ve-x3)/(x2-x3)

def regresionGenetico(p,BD,BR,vE):#Es la regresion normal, pero teniendo en cuenta las reglas activadas y desactivadas
    T=[]# operador de conjunción
    sumaHxPMV=float(0)

    for i in range(len(BR)):
        if(p[i]==1):
            r=BR[i]
            h=[] #Es cada resultado de cada entrada de la regla
            

            for j in range(len(BR[0])):

                if None !=r[j]!="None"  :
                    #Sacamos las coordenadas de cada triangulo
                    x1=BD[j][int(r[j])][0]
                    x2=BD[j][int(r[j])][1]
                    x3=BD[j][int(r[j])][2]

                    h.append(calcularH(x1,x2,x3,float(vE[j])))#ve es el valor de entrada
                    #plt.show()
            
            T.append(min(h))

            #Al ser una figura simétrica, simplemente tenemos que buscar el punto central (xc)
            xc= BD[-1][int(r[-1])][1]
            sumaHxPMV+= min(h)*xc

    if(sum(T)==0): matching=0
    else: matching= sumaHxPMV/sum(T)

    return matching

def regresionCompleta(p,BD,BR,entradas): #Calculamos el matchin del individuo y los devuelve
    matching=[]
    for vE in entradas:
        if(len(vE)>1):
            matching.append(regresionGenetico(p,BD,BR,vE))
    return matching

def errorCuadraticoMedio(entrada,matching):
    sumatorio=0.0
    for i in range(len(entrada)-1):
        sumatorio+=(float(entrada[i][-1])-matching[i])**2
    
    return (sumatorio/len(matching))

def evaluacion(poblacion,BR,entradas,BD):#Se realiza el error cuadratico medio de cada individuo
    ECM=[]

    for p in poblacion:
        matching=regresionCompleta(p,BD,BR,entradas)
        ECM.append(errorCuadraticoMedio(entradas,matching))

    return ECM

def getProbabilidadInversa(errorAux): #Sacamos la probabilidad inversa para que menor error tenga mas probabilidad de elección
    #probabilidadInversa (1/error)/ sum(1/error)
    probabilidadI=[]
    sumDif=0.0
    for e in errorAux:
        sumDif+=(1/e)

    for e in errorAux:
        prob=(1.0/e)/sumDif
        probabilidadI.append(prob)

    return probabilidadI

def buscarPadres(ECM,poblacion):
    #Utilizaremos copias para poder eleminar elementos sin modificar al original
    errorAux=ECM.copy()
    poblacionAux=poblacion.copy()
    padres=[]
    for i in range(2): #Bucle para encontrar a los 2 padres
        probabilidad = getProbabilidadInversa(errorAux) #Buscamos la probabilidad para coger a los mejores padres
        rand=random.random()
        sumaProbabilidad=0.0 
        for j in range(len(probabilidad)) : #Terminara cuando encuentre un padre
            if rand <= (probabilidad[j]+sumaProbabilidad):
                padres.append(poblacionAux[j])
                errorAux.pop(j)
                poblacionAux.pop(j)
                break
            else:
                sumaProbabilidad+=probabilidad[j]

    if(len(padres)!=2): print("error al seleccionar padres")
    return padres

def mutacion(descendiente,numPoblacion): # Se selecciona una posición aleatoria y se cambia esa posición
    pos=random.randrange(0,numPoblacion,1)

    nuevoValor=1-descendiente[pos]# 1-1=0, 1-0=1
    descendiente[pos]=nuevoValor 
    return descendiente

def cruceOX(padres):
    #cojo una sublista del 80% del padre 1
    tamañoSublista=int(len(padres[0])*0.8)
    posInicialSublista=random.randint(0,len(padres[0])-1)
    posFinSubLista=(posInicialSublista+tamañoSublista)%len(padres[0])

    hijo=[None]*len(padres[0])
    for i in range(tamañoSublista):#relleno el hijo con el padre 1
        pos=(posInicialSublista+i)%len(padres[0])
        hijo[pos]=(padres[0][(pos)])


    for i in range(len(hijo)):#relleno el hijo con el padre 
        if(hijo[i]==None):
            hijo[i]=padres[1][i]

    return hijo        

def crearBR(BR,mejor):
    BRmejor=[]
    for i in range(len(mejor)):
        if(mejor[i]==1):
            BRmejor.append(BR[i])

    return BRmejor


def genetico(BR,entradas,BD):

    probabilidadMutacion=0.01
    numPoblacion=21

    #Creamos la población inicial
    poblacion=generarPoblacion(numPoblacion,BR)
    ECM=evaluacion(poblacion,BR,entradas,BD)
    mejorECM=min(ECM)
    posMejor= ECM.index(mejorECM)
    mejor=poblacion[posMejor]
    nuevaPoblacion=[]
    nuevaPoblacionECM=[]

    #Bucle generacional
    generacionesSinMejora=0
    generaciones=0
    while(generaciones<5):
        
        #Bucle para crear una nueva generación
        for i in range(0,len(poblacion),2):
            #Buscamos 2 padres
            padres= buscarPadres(ECM,poblacion)

            #Generamos 2 descendientes con una probabilidad del 90%
            if random.random()<0.9:
                descendientes=[]
                descendientes.append(cruceOX(padres))
                descendientes.append(cruceOX(padres))

                #Zona de mutación
                if random.random()<=probabilidadMutacion:
                    descendientes[0]=mutacion(descendientes[0],numPoblacion)
                if random.random()<=probabilidadMutacion:
                    descendientes[1]=mutacion(descendientes[1],numPoblacion)

                descendientesECM=evaluacion(descendientes,BR,entradas,BD)

                #Introducimos a los hijos en la nueva población
                nuevaPoblacion.append(descendientes[0])
                if(numPoblacion>len(nuevaPoblacion)):
                    nuevaPoblacion.append(descendientes[1])
            
            else: # Los padres pasan a la nueva generación
                nuevaPoblacion.append(padres[0])
                if(numPoblacion>len(nuevaPoblacion)):
                    nuevaPoblacion.append(padres[1])

        nuevaPoblacionECM=evaluacion(nuevaPoblacion,BR,entradas,BD)  
        poblacion=nuevaPoblacion.copy()
        ECM=nuevaPoblacionECM.copy()
        
        #miramos si ha mejorado
        if(mejorECM > min(nuevaPoblacionECM) ):
            mejorECM=min(nuevaPoblacionECM)
            posMejor= ECM.index(mejorECM)
            mejor=poblacion[posMejor]
            # generacionesSinMejora=0
        else:
            #generacionesSinMejora+=1
            print(generacionesSinMejora)

        generaciones+=1

        nuevaPoblacion=[]
        nuevaPoblacionECM=[]   
    print(f"#R mejor: {sum(mejor)}")    
    return crearBR(BR,mejor) #Cuando termine, devlvemos el mejor encontrado



