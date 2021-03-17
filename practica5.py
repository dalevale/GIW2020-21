import requests
import os
from bs4 import BeautifulSoup
url="https://es.wikipedia.org/wiki/Anexo:Cuadros_de_Vel%C3%A1zquez"
r = requests.get(url)
html = r.text
soup = BeautifulSoup(html, 'html.parser')

def porEtapa():
    etapas = list()
    print ("---------Buscar por etapa---------")
    etapas.extend(("Etapa sevillana (hasta 1622)", "Madrid (1622-1629)",
                "Primer viaje a Italia (1629-1630)", "Madrid (1631-1648)",
                "Segundo viaje a Italia (1649-1651)", "Madrid (1651-1660)"))
    for i in range(0, len(etapas)):
        print (str(i+1) + " " + etapas[i])
    op = int(input("Elige una etapa: "))
    if(op < 1) or op > len(etapas):
        print ("Opción invalida!")
    else:
        nombreDir = etapas[op-1]
        if not os.path.exists(nombreDir) and nombreDir != "":
            os.mkdir(nombreDir)
        etapa=etapas[op-1].split()
        etapa="_".join(etapa)
        span = soup.find('span', {"id":etapa})
        pinturas = list()
        tabla = span.parent.next_sibling.next_sibling
        pinturas = list()
        tbody = tabla.contents[1]
        columnas = tbody.contents
        for i in range(2, len(columnas)):
            if((i%2)==0):
                soupImg = BeautifulSoup(str(columnas[i].contents[1].contents[0].contents[0]), "html.parser")
                pintura = dict()
                
                pintura["titulo"] = validarTitulo(columnas[i].contents[3].getText().strip(), pinturas)
                pintura["fecha"] = columnas[i].contents[5].getText().strip()
                pintura["tecnica"] = columnas[i].contents[9].getText().strip()
                pintura["dimensiones"] = columnas[i].contents[7].getText().strip()
                pintura["img"] = soupImg.img['src']
                pintura["observaciones"] = columnas[i].contents[13].getText().strip()
                
                pinturas.append(pintura)
        
        print ("---------Descargando pinturas---------")
        for pintura in pinturas:
            print ("Titulo: " + pintura["titulo"])
            print ("Fecha: " + pintura["fecha"])
            print ("Técnica: " + pintura["tecnica"])
            print ("Dimensiones: " + pintura["dimensiones"])
            print ("Observaciones: " + pintura["observaciones"] + "\n")
            descargarImagen(pintura["img"], pintura["titulo"], nombreDir)

def porTecnica():
    obrasPorTecnica = dict()
    print ("---------Buscar por tecnica---------")
    tablas = soup.find_all("table")
    for i in range(0, len(tablas)):
        tabla = tablas[i]
        tbody = tabla.contents[1]
        columnas = tbody.contents
        for i in range(2, len(columnas)):
            if((i%2)==0):
                tecnica = columnas[i].contents[7].getText().strip()
                soupImg = BeautifulSoup(str(columnas[i].contents[1].contents[0].contents[0]), "html.parser")
                if tecnica == "":
                    tecnica = "Desconocido"
                if tecnica not in obrasPorTecnica:
                    listaDePinturas = list()
                    obrasPorTecnica[tecnica] = listaDePinturas
                
                pintura = dict()
                pintura["titulo"] = validarTitulo(columnas[i].contents[3].getText().strip(), obrasPorTecnica[tecnica])
                pintura["fecha"] = columnas[i].contents[5].getText().strip()
                pintura["dimensiones"] = columnas[i].contents[9].getText().strip()
                pintura["localizacion"] = columnas[i].contents[11].getText().strip()
                pintura["img"] = soupImg.img['src']
                pintura["observaciones"] = columnas[i].contents[13].getText().strip()
                obrasPorTecnica[tecnica].append(pintura)
    claves = list()
    claves.extend(obrasPorTecnica.keys())
    for i in range(0, len(claves)):
        print (str(i+1) + " " + claves[i])
    op = int(input("Elige una tecnica: "))
    if(op < 1) or op > len(claves):
        print ("Opción invalida!")
    else:
        nombreDir = claves[op-1]
        if not os.path.exists(nombreDir) and nombreDir != "":
            os.mkdir(nombreDir)
        print ("---------Descargando pinturas---------")
        pinturas = obrasPorTecnica.get(claves[op-1])
        for pintura in pinturas:
            print ("Titulo: " + pintura["titulo"])
            print ("Fecha: " + pintura["fecha"])
            print ("Localizacion: " + pintura["localizacion"])
            print ("Dimensiones: " + pintura["dimensiones"])
            print ("Observaciones: " + pintura["observaciones"] + "\n")
            descargarImagen(pintura["img"], pintura["titulo"], nombreDir)

def porMuseo():
    obrasPorMuseo = dict()
    print ("---------Buscar por museo---------")
    tablas = soup.find_all("table")
    for i in range(0, len(tablas)):
        tabla = tablas[i]
        tbody = tabla.contents[1]
        columnas = tbody.contents
        for i in range(2, len(columnas)):
            if((i%2)==0):
                museo = columnas[i].contents[11].getText().strip()
                soupImg = BeautifulSoup(str(columnas[i].contents[1].contents[0].contents[0]), "html.parser")
                if museo == "":
                    museo = "Desconocido"
                if museo not in obrasPorMuseo:
                    listaDePinturas = list()
                    obrasPorMuseo[museo] = listaDePinturas
                    
                pintura = dict()
                pintura["titulo"] = validarTitulo(columnas[i].contents[3].getText().strip(), obrasPorMuseo[museo])
                pintura["fecha"] = columnas[i].contents[5].getText().strip()
                pintura["dimensiones"] = columnas[i].contents[9].getText().strip()
                pintura["tecnica"] = columnas[i].contents[7].getText().strip()
                pintura["img"] = soupImg.img['src']
                pintura["observaciones"] = columnas[i].contents[13].getText().strip()
                obrasPorMuseo[museo].append(pintura)
    claves = list()
    claves.extend(obrasPorMuseo.keys())
    for i in range(0, len(claves)):
        print (str(i+1) + " " + claves[i])
    op = int(input("Elige un museo: "))
    if(op < 1) or op > len(claves):
        print ("Opción invalida!")
    else:
        nombreDir = claves[op-1]
        if not os.path.exists(nombreDir) and nombreDir != "":
            os.mkdir(nombreDir)
        print ("---------Descargando pinturas---------")
        pinturas = obrasPorMuseo.get(claves[op-1])
        for pintura in pinturas:
            print ("Titulo: " + pintura["titulo"])
            print ("Fecha: " + pintura["fecha"])
            print ("Técnica: " + pintura["tecnica"])
            print ("Dimensiones: " + pintura["dimensiones"])
            print ("Observaciones: " + pintura["observaciones"] + "\n")
            descargarImagen(pintura["img"], pintura["titulo"], nombreDir)

def existeTitulo(titulo, pinturas):
    ret = False
    for pintura in pinturas:
        if pintura["titulo"] == titulo:
            ret = True
            break
    return ret

def validarTitulo(titulo, pinturas):
    chars = "/\?:*\"<>|"
    for c in chars:
        titulo = titulo.replace(c, "-")
    contador = 0
    while existeTitulo(titulo, pinturas):
        titulo = titulo + "(" + str(contador + 1) + ")"
    return titulo

def descargarImagen(src, titulo, nombreDir):
    res=requests.get("https:" + src)
    try:
        print ("Descargando imagen, " + titulo + "\n")
        res.raise_for_status()
        archivo=open(nombreDir + "/" + titulo + ".jpg", "wb")
        for bloque in res.iter_content(10000):
            archivo.write(bloque)
        archivo.close()
    except:
        print ("Hubo un problema al guardar la imagen, " + titulo + "\n")

def menu():
    while True:
        print("---------Pinturas de Velásquez---------")
        print("1. Buscar por etapa")
        print("2. Buscar por técnica")
        print("3. Buscar por museo")
        print("4. Salir")
    
        op = int(input("Elegir opción: "))
        if op==1:
            porEtapa() 
        elif op==2:
            porTecnica()
        elif op==3:
            porMuseo()
        elif op==4:
            break
        else:
            print("Opción invalida")

menu()
