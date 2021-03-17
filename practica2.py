import json
leer = []
for linea in open('202006_movements.json','r'):
    leer.append(json.loads(linea))
    
#print (linea)

datos = []
def leer():
    for linea in open('202006_movements.json','r'):
        datos.append(json.loads(linea))

def recogidasPorPunto():
    resultado = dict()
    for obj in datos:
        clave = "Punto " + str(obj['idunplug_station'])
        resultado[clave] = resultado.get(clave, 0) + 1
    print(resultado)
    resultadoSort = list()
    for i in range(len(resultado)):
        resultadoSort.append(resultado.get("Punto " + str(i)))
    print (resultadoSort)
    return


def recogidasPorEdad():
    resultado = dict()
    for obj in datos:
        clave = "ageRange " + str(obj['ageRange'])
        resultado[clave] = resultado.get(clave, 0) + 1    
    print(resultado)
    resultadoSort = list()
    for i in range(len(resultado)):
        resultadoSort.append(resultado.get("ageRange " + str(i)))
    print (resultadoSort)
    return
   
def puntoRecYDev():
    resultado = list()
    for obj in datos:
        if not obj["idplug_station"] in resultado:
            if obj["idplug_station"] == obj["idunplug_station"]: 
                resultado.append(obj["idplug_station"])
    resultado.sort()
    print(resultado)
    print(len(resultado))
    return

leer()
recogidasPorEdad()