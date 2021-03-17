# -*- coding: utf-8 -*-

#
# CABECERA AQUI
#

from os import urandom
from flask import Flask, request, session, render_template
from mongoengine import connect, Document, StringField, EmailField, DoesNotExist
from hashlib import sha256
from base64 import b64encode

# Resto de importaciones


app = Flask(__name__)
connect('giw_auth')


# Clase para almacenar usuarios usando mongoengine
class User(Document):
    user_id = StringField(primary_key=True)
    full_name = StringField(min_length=2, max_length=50, required=True)
    country = StringField(min_length=2, max_length=50, required=True)
    email = EmailField(required=True)
    passwd = StringField(required=True)
    salt = StringField(required=True)
    totp_secret = StringField(required=False)


class WrongPasword(Exception):
    pass


##############
# APARTADO 1 #
##############

# 
# Explicación detallada del mecanismo escogido para el almacenamiento de
# contraseñas, explicando razonadamente por qué es seguro
#


def hashPassword(password, salt):
    salted_password = password.encode('utf-8') + salt
    hashed_password = str(sha256(salted_password).digest())
    return hashed_password


@app.route('/signup', methods=['POST'])
def signup():
    contenido = request.form
    nickname = contenido['nickname']
    salt = b64encode(urandom(32))
    try:
        User.objects.get(user_id=nickname)
        return "El usuario ya existe.", 200
    except DoesNotExist:
        password_hashed = hashPassword(contenido['password'], salt)
        password2_hashed = hashPassword(contenido['password'], salt)
        if password_hashed != password2_hashed:
            return "Las contraseñas no coinciden", 200

        full_name = contenido['full_name']
        u = User(user_id=nickname, full_name=contenido['full_name'],
                 country=contenido['country'], email=contenido['email'],
                 passwd=password_hashed, salt=salt.decode())
        u.save()
        return "Bienvenido usuario " + full_name, 200


@app.route('/change_password', methods=['POST'])
def change_password():
    contenido = request.form
    nickname = contenido['nickname']
    salt = b64encode(urandom(32))
    try:
        u = User.objects.get(user_id=nickname)
        if hashPassword(contenido['old_password'], u.salt.encode()) != u.passwd:
            raise WrongPasword
        u.passwd = hashPassword(contenido['new_password'], salt)
        u.save()
        ret = 'La contraseña del usuario ' + nickname + " ha sido modificada."
    except (DoesNotExist, WrongPasword):
        ret = 'Usuario o contraseña incorrectos'

    return ret, 200


@app.route('/login', methods=['POST'])
def login():
    contenido = request.form
    nickname = contenido['nickname']
    try:
        u = User.objects.get(user_id=nickname)
        if hashPassword(contenido['password'], u.salt.encode()) != u.passwd:
            raise WrongPasword
        ret = 'Bienvenido ' + nickname
    except (DoesNotExist, WrongPasword):
        ret = 'Usuario o contraseña incorrectos'

    return ret, 200
    

##############
# APARTADO 2 #
##############

# 
# Explicación detallada de cómo se genera la semilla aleatoria, cómo se construye
# la URL de registro en Google Authenticator y cómo se genera el código QR
#


@app.route('/signup_totp', methods=['POST'])
def signup_totp():
    pass
        

@app.route('/login_totp', methods=['POST'])
def login_totp():
    pass
  

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
