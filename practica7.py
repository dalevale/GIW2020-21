"""
GIW 2020-21
Práctica 07
Grupo 05
Autores: XX, YY, ZZ,
(Nombres completos de los autores) declaramos que esta solución es fruto exclusivamente
de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos
obtenido la solución de fuentes externas, y tampoco hemos compartido nuestra solución
con nadie. Declaramos además que no hemos realizado de manera deshonesta ninguna otra
actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.
"""
from flask import Flask, request

app = Flask(__name__)

# Variable global donde se almacena la lista de asignaturas
asignaturas = list()

# Listas de claves para comparar las claves de JSON que viene desde el navegador
claves_asig = ['nombre', 'numero_alumno', 'horario']
claves_horario = ['dia', 'hora_inicio', 'hora_final']
ctr = 0


# Se borra la lista entera de asignaturas
@app.route('/asignaturas', methods=['DELETE'])
def borrar_asignaturas():
    asignaturas.clear()
    return 'DELETE', 204


# Función para añadir una asignatura en la lista con las datos que reciben
# Primero se comparan las claves que se recibe con las claves almaacenadas
# en los variables globales definidos
@app.route('/asignaturas', methods=['POST'])
def anadir_asignaturas():
    global ctr
    respuesta = dict()
    ret = 201
    asignatura = dict()
    horarios = list()
    contenido = request.get_json()
    for clave in claves_asig:
        if clave not in contenido.keys():
            ret = 400
    if ret != 400:
        horarios_contenido = contenido['horario']
        for horario_contenido in horarios_contenido:
            for clave in claves_horario:
                if clave not in horario_contenido.keys():
                    ret = 400
            if ret != 400:
                horario = dict()
                horario['dia'] = horario_contenido['dia']
                horario['hora_inicio'] = horario_contenido['hora_inicio']
                horario['hora_final'] = horario_contenido['hora_final']
                horarios.append(horario)

    if ret != 400:
        asignatura['id'] = ctr
        asignatura['nombre'] = contenido['nombre']
        asignatura['numero_alumno'] = contenido['numero_alumno']
        asignatura['horarios'] = horarios
        asignaturas.append(asignatura)
        ctr += 1
        respuesta['id'] = asignatura['id']
    return respuesta, ret


# Funcion que gobierna las peticiones con el método 'GET'
# Primero comprueba si se asignan valores en los parametros 'page', 'per_page'
# y 'alumnos_gte'. Los 3 parametros pueden exisitir la vez pero 'page' y
# 'per_page' tienen que exisitir juntos. Después se calcula el numero
# de paginas que puede haber donde cada página hay 'per_page' numero de
# asignaturas, si el número de paginas es menor que 'page', error.
@app.route('/asignaturas', methods=['GET'])
def asignaturas_paginacion():
    ids = list()
    respuesta = dict()
    pagina = request.args.get('page')
    por_pagina = request.args.get('per_page')
    num_alumnos = request.args.get('alumnos_gte')
    ret = 200
    asignaturas_aux = asignaturas
    if num_alumnos is not None:
        num_alumnos = int(num_alumnos)
        asignaturas_aux = list()
        for asignatura in asignaturas:
            if asignatura['numero_alumno'] >= num_alumnos:
                asignaturas_aux.append(asignatura)
    if len(asignaturas_aux) != len(asignaturas):
        ret = 206
    if ((pagina is not None) & (por_pagina is None)) | ((pagina is None) & (por_pagina is not None)):
        ret = 400
    elif (pagina is not None) & (por_pagina is not None):
        pagina = int(pagina)
        por_pagina = int(por_pagina)
        num_asignaturas = len(asignaturas_aux)
        num_paginas = num_asignaturas // por_pagina
        if num_asignaturas % por_pagina != 0:
            num_paginas += 1
        if num_paginas < pagina:
            ret = 400
        else:
            ini = por_pagina * (pagina - 1)
            fin = ini + por_pagina
            for i in range(ini, fin):
                if i < num_asignaturas:
                    ids.append("/asignaturas/" + str(asignaturas_aux[i]['id']))
    else:
        for asignatura in asignaturas_aux:
            ids.append("/asignaturas/" + str(asignatura['id']))
    respuesta['asignaturas'] = ids
    return respuesta, ret


# Funcion donde se modifica una asignatura con el id 'id_asignatura'
# Primero se comprueba si existe una asignatura con el id 'id_asignatura'
# Si existe, dependiendo del método, se implementa una cierta función
@app.route('/asignaturas/<int:id_asignatura>', methods=['DELETE', 'GET', 'PUT', 'PATCH'])
def modificar_asignatura(id_asignatura):
    ret = 200
    response = ''
    existe = False
    for asignatura in asignaturas:
        if asignatura['id'] == id_asignatura:
            asignatura_mod = asignatura
            existe = True
            break
    if not existe:
        return '', 404
    if request.method == 'DELETE':
        asignaturas.remove(asignatura_mod)
        ret = 204
    elif request.method == 'GET':
        response = asignatura_mod
    elif request.method == 'PUT':
        asignatura = dict()
        horarios = list()
        contenido = request.get_json()
        for clave in claves_asig:
            if clave not in contenido.keys():
                ret = 400
        if ret != 400:
            horarios_contenido = contenido['horario']
            for horario_contenido in horarios_contenido:
                for clave in claves_horario:
                    if clave not in horario_contenido.keys():
                        ret = 400
                if ret != 400:
                    horario = dict()
                    horario['dia'] = horario_contenido['dia']
                    horario['hora_inicio'] = horario_contenido['hora_inicio']
                    horario['hora_final'] = horario_contenido['hora_final']
                    horarios.append(horario)
        if ret != 400:
            asignatura['id'] = id_asignatura
            asignatura['nombre'] = contenido['nombre']
            asignatura['numero_alumno'] = contenido['numero_alumno']
            asignatura['horarios'] = horarios
            asignaturas.remove(asignatura_mod)
            asignaturas.append(asignatura)
    elif request.method == 'PATCH':
        contenido = request.get_json()
        clave = contenido.keys()[0]
        if clave not in claves_asig:
            ret = 400
        else:
            index = asignaturas.index(asignatura_mod)
            asignaturas[index][clave] = contenido[clave]
    return response, ret


# Función que busca el horario de una asignatura con id 'id_numero'
# y se retorna el horario si la asignatura existe.
@app.route('/asignaturas/<int:numero>', methods=['GET'])
def horario_asignatura(id_asignatura):
    ret = 200
    response = ''
    existe = False
    for asignatura in asignaturas:
        if asignatura['id'] == id_asignatura:
            asignatura_mod = asignatura
            existe = True
            break
    if not existe:
        return '', 404
    response = asignatura_mod['horario']
    return response, ret


class FlaskConfig:
    """Configuración de Flask"""
    # Activa depurador y recarga automáticamente
    ENV = 'development'
    DEBUG = True
    TEST = True
    # Imprescindible para usar sesiones
    SECRET_KEY = "giw2020&!_()"
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


if __name__ == '__main__':
    app.config.from_object(FlaskConfig())
    app.run()
