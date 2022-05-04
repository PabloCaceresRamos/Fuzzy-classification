import numpy as np
import matplotlib.pyplot as plt

from genetico import evaluacion

def crearBaseDatos(RangosEntradas,nE):#nE es el numero de entradas

    #Vamos a sacar las etiquetas de cada entrada
    #Para ello vamos a dividir el rango en el numero de etiquetas
    # Para que se solapen las etiquetas se aumentan un 10% por la izquierda y por la derecha

    #fig, ax = plt.subplots(len(RangosEntrada))
    

    BD=[0]*len(RangosEntradas) # Base de datos (BD)

    for i in range(len(RangosEntradas)):
        li=RangosEntradas[i][0] #cogemos el limite inferior
        ls=RangosEntradas[i][1]#cogemos el limite superior
        BD[i]=[None]*nE
        tamañoEtiqueta=(ls-li)/nE
        
        #Asignamos la primera etiqueta de la entrada a la base de datos
        BD[i][0]=[0]*3
        BD[i][0][0]=li
        BD[i][0][1]=li
        if(li+tamañoEtiqueta)>0:BD[i][0][2]=(li+tamañoEtiqueta)*1.05 #Los positivos los multiplico por 1.05 para que agranden
        else:BD[i][0][2]=(li+tamañoEtiqueta)*0.95 #Los positivos los multiplico por 0.95 para que agranden
        #ax[i].plot([BD[i][0][0],BD[i][0][1],BD[i][0][2]],[0,1,0])

        #Asignamos de la 2º etiqueta a la nE-1
        maxAnterior =li+tamañoEtiqueta

        for n in range(1,nE-1):
            BD[i][n]=[0]*3
            if(maxAnterior)>0:BD[i][n][0]=maxAnterior * 0.95 
            else:BD[i][n][0]=maxAnterior * 1.05 
            BD[i][n][1]=maxAnterior+(tamañoEtiqueta/2)
           
            if(maxAnterior+tamañoEtiqueta)>0: BD[i][n][2]=(maxAnterior+tamañoEtiqueta)*1.05
            else: BD[i][n][2]=(maxAnterior+tamañoEtiqueta)*0.95
            maxAnterior=maxAnterior+tamañoEtiqueta

            #ax[i].plot([BD[i][n][0],BD[i][n][1],BD[i][n][2]],[0,1,0])
            

        #Asignamos la ultima etiqueta
        BD[i][-1]=[0]*3
        if(maxAnterior>0): BD[i][-1][0]=maxAnterior*0.95
        else:BD[i][-1][0]=maxAnterior*1.05
        BD[i][-1][1]=ls
        BD[i][-1][2]=ls

        #ax[i].plot([BD[i][-1][0],BD[i][-1][1],BD[i][-1][2]],[0,1,0])
    plt.show()

    return BD

def crearBaseDatos2(RangosEntradas,nE):#Etiquetas sin solapamiento

    #Vamos a sacar las etiquetas de cada entrada
    #Para ello vamos a dividir el rango en el numero de etiquetas
    # de lo que le pertenece par aque queden solapadas

    #fig, ax = plt.subplots(len(RangosEntrada))
    

    BD=[0]*len(RangosEntradas) # Base de datos (BD)

    for i in range(len(RangosEntradas)):
        li=RangosEntradas[i][0] #cogemos el limite inferior
        ls=RangosEntradas[i][1]#cogemos el limite superior
        BD[i]=[None]*nE
        tamañoEtiqueta=(ls-li)/nE
        
        #Asignamos la primera etiqueta de la entrada a la base de datos
        BD[i][0]=[0]*3
        BD[i][0][0]=li
        BD[i][0][1]=li
        BD[i][0][2]=(li+tamañoEtiqueta)
        #ax[i].plot([BD[i][0][0],BD[i][0][1],BD[i][0][2]],[0,1,0])

        #Asignamos de la 2º etiqueta a la nE-1
        maxAnterior =li+tamañoEtiqueta

        for n in range(1,nE-1):
            BD[i][n]=[0]*3
            BD[i][n][0]=maxAnterior 
            BD[i][n][1]=maxAnterior+(tamañoEtiqueta/2)
            BD[i][n][2]=(maxAnterior+tamañoEtiqueta)
            maxAnterior=maxAnterior+tamañoEtiqueta

            #ax[i].plot([BD[i][n][0],BD[i][n][1],BD[i][n][2]],[0,1,0])
            

        #Asignamos la ultima etiqueta
        BD[i][-1]=[0]*3
        BD[i][-1][0]=maxAnterior
        BD[i][-1][1]=ls
        BD[i][-1][2]=ls

       # ax[i].plot([BD[i][-1][0],BD[i][-1][1],BD[i][-1][2]],[0,1,0])
    #plt.show()

    return BD

def leerFichero(nombreFich):
    lectura = open(nombreFich,"r")
    fichero=lectura.read().split("\n")
    fich =[]
    for i in range(15,len(fichero)):#Recorremos todo el fichero saltando las lineas de información
        linea = fichero[i].split(",")#Separamo todos los datos de cada linea
        fich.append(linea)
    
    lectura.close()
    return fich #Devolvemos una tabla con cada linea y cada dato separado

def rellenarGradoCerteza(BR):

    for i in range(len(BR)):#Iremos regla por regla asignandole su grado de certeza
        contaIguales=0
        contadorAntecedentesIguales=0

        for j in range(len(BR)):#Iremos regla por regla buscando cuales son iguales y cuales no
            if(np.array_equal(BR[i][0:(len(BR[0])-1)],BR[j][0:(len(BR[0])-1)])):#Miramos si son iguales
                contaIguales+=1
                contadorAntecedentesIguales+=1
            elif(np.array_equal(BR[i][0:(len(BR[0])-2)],BR[j][0:(len(BR[0])-2)])):#Miramos si los antecedentes son iguales
                contadorAntecedentesIguales+=1

        BR[i][-1]=contaIguales/contadorAntecedentesIguales

def mayorPertenencia(e1,e2,ve,y1,y2):#Devolvemos la "y" de la etiqueta a la cual el punto ve pertenece mas
    if calcularH(e1[0],e1[1],e1[2],ve) < calcularH(e2[0],e2[1],e2[2],ve):
        return y2
    else:
        return y1

def chi96(fich,numMuestras,BD):

    BR=[]
    for i in range(len(fich)-1): #Miramos cada linea del fichero leido. La ultima linea esta vacia, por eso vamos hasta len-1
        r=[None]*(numMuestras+2)#Tenemos los antecendentes, la clase y el grado de certeza

        for j in range (numMuestras): #En cada linea miramos cada campo de los antecedentes
            
            for y in range(len(BD[j])): #Miramos todas las figuras hasta encontrar una que contenga al campo j leido

                if min(BD[j][y])< float(fich[i][j])<= max(BD[j][y]):  #Si encontramos la figura la guardamos y salimos del bucle de y
                    if(y<len(BD[j])-1 ):#Miramos que no sea la ultima etiqueta
                        if(min(BD[j][y+1])< float(fich[i][j])<= max(BD[j][y+1])):# Si tambien pertenece a la siguiente etiqueta
                            #Miramos a cual etiqueta pertenece mas el punto y le asignamos la etiqueta
                            r[j]=mayorPertenencia(BD[j][y],BD[j][y+1],float(fich[i][j]),y,y+1)   
                            break     
                    #Asignamos el punto a la etiqueta encontrada
                    r[j]=y
                    break

        r[-2]=int(fich[i][-1])    
        BR.append(r)

    rellenarGradoCerteza(BR) #Rellenara el grado de certeza de todas las reglas
    
    return BR

def chi96_2(fich,numMuestras,BD):#No tiene en cuenta el solapamiento de las etiquetas

    BR=[]
    for i in range(len(fich)-1): #Miramos cada linea del fichero leido. La ultima linea esta vacia, por eso vamos hasta len-1
        r=[None]*(numMuestras+2)#Tenemos los antecendentes, la clase y el grado de certeza

        for j in range (numMuestras): #En cada linea miramos cada campo de los antecedentes
            
            for y in range(len(BD[j])): #Miramos todas las figuras hasta encontrar una que contenga al campo j leido

                if min(BD[j][y])< float(fich[i][j])<= max(BD[j][y]):  #Si encontramos la figura la guardamos y salimos del bucle de y
                    r[j]=y
                    break

        r[-2]=int(fich[i][-1])    
        BR.append(r)

    rellenarGradoCerteza(BR) #Rellenara el grado de certeza de todas las reglas
    
    return BR

def quitarReglasDuplicadas(BR):#Quitamos de la base de reglas las repetidas y que no tengan una salida valida
    BRsimplificada=[]
    for r in BR:
        repetido=False
        for j in BRsimplificada:
            if np.array_equal(r,j): #Si la regla esta duplicada nos salimos del bucle j y no la metemos
                repetido=True
                break

        if not repetido and r[-1]!=None: #Añadimos las reglas con salidas valida y que no esten repetidas
            BRsimplificada.append(r)

    
    return BRsimplificada

def crearFicheroReglas(nE,BR,n):
    nombreFichero="Reglas Clasificacion "+str(nE)+" etiquetas"+ str(n)

    np.savetxt(nombreFichero,BR,fmt="%s") #Crea el fichero con la base de reglas

    print("Fichero de reglas creado")

def leerFicheroReglas(nE,n):

    nombreFichero="Reglas Clasificacion "+str(nE)+" etiquetas"+ str(n)

    lectura = open(nombreFichero,"r")
    fichero=lectura.read().split("\n")
    BRleida =[]
    for i in range(len(fichero)-1):#Recorremos todo el fichero
        linea = fichero[i].split(" ")#Separamo todos los datos de cada linea
        BRleida.append(linea)
    
    lectura.close()
    return BRleida 

def clasificacion(BD,BR,vE):
    GA=[]# Grado asociación
    sumaHxPMV=float(0)

    for i in range(len(BR)):
        r=BR[i]
        h=[] #Es cada resultado de cada entrada de la regla
        

        for j in range(len(BR[0])-2):

             if None !=r[j]!="None"  :
                #Sacamos las coordenadas de cada triangulo
                x1=BD[j][int(float(r[j]))][0]
                x2=BD[j][int(float(r[j]))][1]
                x3=BD[j][int(float(r[j]))][2]

                h.append(calcularH(x1,x2,x3,float(vE[j])))#ve es el valor de entrada
        
        GA.append(min(h)* float( r[-1] ))

        maxGApos=GA.index(max(GA)) #Me quedo con la regla con mayor GA
        clase=float(BR[maxGApos][-2])

    return [clase,GA[maxGApos]]

def calcularH(x1,x2,x3,ve):

    
    if ve<x1: 
        return 0
    if(ve>x3): 
        return 0
    if(ve==x2): 
        return 1
    if ve<x2: 
        return (ve-x1)/(x2-x1)
    else: 
        return (ve-x3)/(x2-x3)

def evaluacionClasificacion(matching,test):#Dividimos las predicciones correctas entre el total
    Tpred=0
    total=0
    for i in range(len(matching)):
        if(len(test[i])>1):
            total+=1
            if(matching[i][0]==int(test[i][-1])):
                Tpred+=1

    return Tpred/total



#main

#Rangos de los campos introducidos
RI=[1.5111499,1.53393]
Na=[10.7299,17.38]
Mg=[-0.001,4.49]
Al=[0.2899,3.5]
Si=[69.8099,75.41]
K=[-0.001,6.21]
Ca=[5.4299,16.19]
Ba=[-0.001,3.15]
Fe=[-0.001,0.51]
RangosEntrada=[RI,Na,Mg,Al,Si,K,Ca,Ba,Fe]

nE=5   #Número de etiquetas que utilizaremos (triangulos)
BD=crearBaseDatos(RangosEntrada,nE)

nombreFicheros="./DataSet/glass-5dobscv-"
evaluacion=[None]*5

"""for nfichero in range(1,6):
    #########################################                   Train                     ###############################

    nomb=nombreFicheros+str(nfichero)+"tra.dat"
    ficheroTrain=leerFichero(nomb)
    BRprimaria=chi96(ficheroTrain,len(RangosEntrada),BD)
    BR=quitarReglasDuplicadas(BRprimaria)

    crearFicheroReglas(nE,BR,nfichero)"""

for nfichero in range(1,6):
    #########################################                   Test                     #################################

    nomb=nombreFicheros+str(nfichero)+"tst.dat"
    BR=leerFicheroReglas(nE,nfichero)
    print(f"reglas: {len(BR)}")
    test=leerFichero(nomb)
    matching=[]
    for vE in test: #Recorremos cada linea del fichero test
        if len(vE)!= 1:#El ultimo campo lo lee vacio, para que no de error, colocamos el if
            matching.append(clasificacion(BD,BR,vE))

    evaluacion[nfichero-1]=evaluacionClasificacion(matching,test)

print(evaluacion)
print(f"Error medio: {sum(evaluacion)/len(evaluacion)}")