## import urllib.request
import json
import os
from urllib.parse import urlencode, quote_plus
from IPython.display import Image, display

def validarTitulo(titulo):
    chars = "/\?:*\"<>|"
    for c in chars:
        titulo = titulo.replace(c, "-")
    return titulo

def descargarImagen(src, titulo, nombreDir):
    try:
        archivo=open(nombreDir + "/" + titulo + ".jpg", "wb")
        
        img=urllib.request.urlopen(src)

        while True:
            info=img.read(100000)
            if len(info)<1: 
                break
            archivo.write(info)
        archivo.close()
    except:
        print ("Hubo un problema al guardar la imagen, " + titulo + "\n")

def opcion1(nombre):
    clave="19d750a9"
    uri="http://www.omdbapi.com/?apikey="+clave
    url = uri + "&"+urlencode({"s":nombre, "type":"movie"},quote_via=quote_plus)
    manf = urllib.request.urlopen(url)
    
    if(manf.getcode()==200):
        datos = manf.read()
        jsonDatos = json.loads(datos)
        
        print ("\033[1m-----Resultado-----\033[1m")
        for pelicula in jsonDatos['Search']:
            titulo = pelicula['Title']
            anio = pelicula['Year']
            peliID = pelicula['imdbID']
            tipo = pelicula['Type']
            poster = pelicula['Poster']
            print ("\033[1mTítulo:\033[0m " + titulo)
            print ("\033[1mAño:\033[0m " + anio)
            print ("\033[1mID imdb:\033[0m " + peliID)
            print ("\033[1mTipo:\033[0m " + tipo)
            print ("\033[1mPoster:\033[0m " + poster + "\n")
            
def opcion2(peliID):
    clave="19d750a9"
    uri="http://www.omdbapi.com/?apikey="+clave
    url = uri + "&"+urlencode({"i":"tt3896198"},quote_via=quote_plus)
    manf = urllib.request.urlopen(url)
  
    if(manf.getcode()==200):
        datos = manf.read()
        pelicula = json.loads(datos)
        
        print ("\033[1m-----Resultado-----\033[0m")
        print ("\033[1mTítulo:\033[0m " + pelicula['Title'])
        print ("\033[1mAño:\033[0m " + pelicula['Year'])
        print ("\033[1mCategoría:\033[0m " + pelicula['Rated'])
        print ("\033[1mFecha release:\033[0m " + pelicula['Released'])
        print ("\033[1mDuración:\033[0m " + pelicula['Runtime'])
        print ("\033[1mDirector:\033[0m " + pelicula['Director'])
        print ("\033[1mAutor:\033[0m " + pelicula['Writer'])
        print ("\033[1mActores:\033[0m " + pelicula['Actors'])
        print ("\033[1mTrama:\033[0m " + pelicula['Plot'])
        print ("\033[1mPaís:\033[0m " + pelicula['Country'])
        print ("\033[1mLenguaje:\033[0m " + pelicula['Language'])
        print ("\033[1m---Calificaciones---\033[0m")
        for fuente in pelicula['Ratings']:
            print ("\033[1mFuente:\033[0m " + fuente['Source'])
            print ("\033[1mCalificación:\033[0m " + fuente['Value'] + "\n")
        print ("\033[1mMetascore:\033[0m " + pelicula['Metascore'])
        print ("\033[1mCalificación imdb:\033[0m " + pelicula['imdbRating'])
        print ("\033[1mVotos imdb:\033[0m " + pelicula['imdbVotes'])
        print ("\033[1mID imdb:\033[0m " + pelicula['imdbID'])
        print ("\033[1mTipo:\033[0m " + pelicula['Type'])
        print ("\033[1mDVD:\033[0m " + pelicula['DVD'])
        print ("\033[1mBox Office:\033[0m " + pelicula['BoxOffice'])
        print ("\033[1mProducción:\033[0m " + pelicula['Production'])
        print ("\033[1mWebsite:\033[0m " + pelicula['Website'] + "\n")
        
def opcion3(nombre):
    clave="19d750a9"
    uri="http://www.omdbapi.com/?apikey="+clave
    url = uri + "&"+urlencode({"s":nombre, "type":"movie"},quote_via=quote_plus)
    manf = urllib.request.urlopen(url)
    
    if(manf.getcode()==200):
        datos = manf.read()
        jsonDatos = json.loads(datos)
        
        for pelicula in jsonDatos['Search']:
            buscarPorID(pelicula['imdbID'])

def opcion4(nombre):
    clave="19d750a9"
    uri="http://www.omdbapi.com/?apikey="+clave
    url = uri + "&"+urlencode({"s":nombre, "type":"movie"},quote_via=quote_plus)
    manf = urllib.request.urlopen(url)
    nombreDir = "Posters"
    
    if(manf.getcode()==200):
        if not os.path.exists(nombreDir) and nombreDir != "":
            os.mkdir(nombreDir)
        datos = manf.read()
        jsonDatos = json.loads(datos)
        
        print ("\033[1m-----Resultado-----\033[0m")
        for pelicula in jsonDatos['Search']:
            titulo = pelicula['Title']
            poster = pelicula['Poster']
            print("\033[1mTítulo:\033[0m " + titulo)
            print("\033[1mPoster:\033[0m " + poster)
            if poster != "N/A":
                titulo = validarTitulo(titulo)
                descargarImagen(poster, titulo, nombreDir)
    
def opcion5(nombre):
    nombreDir = "Posters"
    clave="19d750a9"
    uri="http://www.omdbapi.com/?apikey="+clave
    url = uri + "&"+urlencode({"s":nombre, "type":"movie"},quote_via=quote_plus)
    manf = urllib.request.urlopen(url)
    
    if(manf.getcode()==200):
        datos = manf.read()
        jsonDatos = json.loads(datos)
        
        print ("\033[1m-----Resultado-----\033[0m")
        peliculas = list()
        contador = 0
        for pelicula in jsonDatos['Search']:
            contador += 1
            peli = dict()
            peli['titulo'] = pelicula['Title']
            peli['imdbID'] = pelicula['imdbID']
            peli['poster'] = pelicula['Poster']
            peliculas.append(peli)
            print(str(contador) + " " + pelicula['Title'])
        peliNum = int(input("Escoge numero de la pelicula: "))
        peliTitulo = peliculas[peliNum]['titulo']
        peliPoster = peliculas[peliNum]['poster']
        peliID = peliculas[peliNum]['imdbID']
        print("\033[1m-------Poster-------\033[0m")
        if peliPoster != "N/A":
            if not os.path.exists(nombreDir) and nombreDir != "":
                os.mkdir(nombreDir)
            descargarImagen(peliPoster, peliTitulo, nombreDir)
            nomPoster = nombreDir + "/" + peliTitulo + ".jpg"
            display(Image(filename=nomPoster))
        else:
            print("Esta película no tiene poster")
        opcion2(peliID)         
    
def menu():
    while True:
        print("\033[1m----------Menu----------\033[0m")
        print("1: Buscar por Nombre de la Película")
        print("2: Buscar por ID de la Película")
        print("3: Busqueda Ampliada")
        print("4: Recuperar posters")
        print("5: Recuperar película con poster")
        print("6: Salir")
        op = int(input("Elige opción: "))
        
        if(op == 1):
            opcion1(input("Nombre de la película: "))
        elif(op == 2):
            opcion2(input("ID de la película: "))
        elif(op == 3):
            opcion3(input("Nombre de la película: "))
        elif(op == 4):
            opcion4(input("Nombre de la película: "))
        elif(op == 5):
            opcion5(input("Nombre de la película: "))
        elif(op == 6):
            break
        else:
            print("Opción invalida")
            
menu()