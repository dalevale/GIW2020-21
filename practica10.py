# -*- coding: utf-8 -*-

"""
GIW 2020-21
Práctica 10
Grupo 05
Autores: Francisco García Navarrete, Harold Luis Pascua Cajucom, Ari Rubén Simao Chaves, Dale Francis Valencia Calicdan

Francisco García Navarrete, Harold Luis Pascua Cajucom, Ari Rubén Simao Chaves y Dale
Francis Valencia Calicdan declaramos que esta solución es fruto exclusivamente de nuestro
trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la
solución de fuentes externas, y tampoco hemos compartido nuestra solución con nadie.
Declaramos además que no hemos realizado de manera deshonesta ninguna otra actividad que
pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.
"""

from flask import Flask, request, session
from requests import post, get
from time import time

app = Flask(__name__)

# Credenciales.
# https://developers.google.com/identity/protocols/oauth2/openid-connect#appsetup
# Copiar los valores adecuados.
CLIENT_ID = "858922529382-2ren3nppibe080k5q6udk6mhl9a7nsu5.apps.googleusercontent.com"
CLIENT_SECRET = "HwjpR9IGxyUCCS9wTRYHU5Qo"

REDIRECT_URI = 'http://localhost:5000/token'

# Fichero de descubrimiento para obtener el 'authorization endpoint' y el
# 'token endpoint'
# https://developers.google.com/identity/protocols/oauth2/openid-connect#authenticatingtheuser
DISCOVERY_DOC = 'https://accounts.google.com/.well-known/openid-configuration'

# token_info endpoint para extraer información de los tokens en depuracion, sin
# descifrar en local
# https://developers.google.com/identity/protocols/OpenIDConnect#validatinganidtoken
TOKENINFO_ENDPOINT = 'https://oauth2.googleapis.com/tokeninfo'

# Información del fichero de descubrimiento usada para hacer las validaciones
discovery = get(DISCOVERY_DOC).json()
auth_endpt = discovery["authorization_endpoint"]
token_endpt = discovery["token_endpoint"]
uri_claves = discovery["jwks_uri"]
issuer = discovery["issuer"]


@app.route('/login_google', methods=['GET'])
def login_google():
    url = f"{auth_endpt}?" \
          "response_type=code&" \
          f"client_id={CLIENT_ID}&" \
          "scope=openid%20email&" \
          f"redirect_uri={REDIRECT_URI}"
    html = f"<a href={url}>Haga clic aquí para autenticarse</a>"

    return html, 200


@app.route('/token', methods=['GET'])
def token():
    url_post = f"{token_endpt}?code={request.args['code']}&" \
               f"client_id={CLIENT_ID}&" \
               f"client_secret={CLIENT_SECRET}&" \
               f"redirect_uri={REDIRECT_URI}&" \
               "grant_type=authorization_code"

    id_token = post(url_post).json()["id_token"]
    url_get = f"{TOKENINFO_ENDPOINT}?id_token={id_token}"
    jwt = get(url_get).json()

    # Verificar
    keys = get(uri_claves).json()["keys"]
    if jwt["kid"] not in [key["kid"] for key in keys]:
        return "ERROR: ", 200

    if jwt["iss"] not in [issuer, issuer.strip("https://")]:
        return "ERROR: Emisor inválido", 200

    if jwt["aud"] != CLIENT_ID:
        return "ERROR: ID de cliente inválida", 200

    if int(jwt["exp"]) < int(time()):
        return "ERROR: ID token caducada", 200

    return f"Bienvenido {jwt['email']}", 200


class FlaskConfig:
    '''Configuración de Flask'''
    # Activa depurador y recarga automáticamente
    ENV = 'development'
    DEBUG = True
    TEST = True
    # Imprescindible para usar sesiones
    SECRET_KEY = 'giw2020&!_()'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


if __name__ == '__main__':
    app.config.from_object(FlaskConfig())
    app.run()