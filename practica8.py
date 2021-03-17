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
from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, ComplexDateTimeField
from mongoengine import StringField, IntField, FloatField, ListField, ReferenceField, ValidationError
from mongoengine import connect
connect("giw_mongoengine")


letras = ['T', 'R', 'W', 'A', 'G', 'M', 'Y', 'F', 'P', 'D', 'X', 'B', 'N', 'J', 'Z',
          'S',  'Q', 'V', 'H', 'L', 'C', 'K', 'E']


class Producto(Document):
    codigo_barras = StringField(primary_key=True, min_length=13, max_length=13, regex="^[0-9]*$")
    nombre = StringField(required=True, min_length=2)
    categoria_principal = IntField(required=True, min_value=0)
    categorias_secundarias = ListField(IntField(min_value=0))

    def clean(self):
        self.validate(clean=False)
        if len(self.categorias_secundarias) == 0 | self.categoria_principal != self.categorias_secundarias[0]:
            raise(ValidationError("La categoría principal no coincide con la primera categoría "
                                  "en la lista de categorías secundarias!"))
        cifra_ultima = int(self.codigo_barras[12])
        suma = 0
        for i in range(12):
            if i % 2 == 0:
                suma += int(self.codigo_barras[i])
            else:
                suma += int(self.codigo_barras[i])*3
        if (suma + cifra_ultima) % 10 != 0:
            raise(ValidationError("Formato del código de barra invalido!"))


class Linea(EmbeddedDocument):
    num_items = IntField(required=True, min_value=0)
    precio_item = FloatField(required=True, min_value=0)
    name = StringField(required=True, min_length=2)
    total = FloatField(required=True, min_value=0)
    ref = ReferenceField(Producto, required=True)

    def clean(self):
        self.validate(clean=False)
        suma_precio = self.num_items * self.precio_item
        if suma_precio != self.total:
            raise(ValidationError("El precio total no coincide con el precio del"
                                  "producto multiplicado por la cantiad!"))

        if self.name != self.ref.nombre:
            raise(ValidationError("El nombre del producto no coincide con el de la "
                                  "referencia al producto!"))


class Pedido(Document):
    total = FloatField(required=True, min_value=0)
    fecha = ComplexDateTimeField(required=True)
    lineas = ListField(EmbeddedDocumentField(Linea), required=True)

    def clean(self):
        self.validate(clean=False)
        suma_precio = 0
        for linea in self.lineas:
            suma_precio += linea.total
        if suma_precio != self.total:
            raise(ValidationError("El precio total no coincide con el precio "
                                  "total sumando los precios de los productos!"))
        nombre_productos = list()
        for linea in self.lineas:
            if linea.name in nombre_productos:
                raise(ValidationError("Existen 2 lineas de pedidos con el mismo nombre de producto!"))
            else:
                nombre_productos.append(linea.name)


class Tarjeta(EmbeddedDocument):
    nombre = (StringField(required=True, min_length=2, regex="[A-Z]+[a-z]"))
    numero = (StringField(primary_key=True, min_length=16, max_length=16, regex="^[0-9]+$"))
    mes = (StringField(required=True, min_length=2, max_length=2, choices=['01', '02', '03', '04', '05', '06', '07',
                                                                           '08', '09', '10', '11', '12']))
    año = (StringField(required=True, min_length=2, max_length=2, regex="^[0-9]+$"))
    ccv = (StringField(required=True, min_length=3, max_length=3, regex="^[0-9]+$"))


class Usuario(Document):
    dni = (StringField(primary_key=True, min_length=9, max_length=9))
    nombre = (StringField(required=True, min_length=2, regex="[A-Z]+[a-z]"))
    apellido1 = (StringField(required=True, min_length=2, regex="[A-Z]+[a-z]"))
    apellido2 = (StringField(min_length=2, regex="[A-Z]+[a-z]"))
    f_nac = StringField(required=True, min_length=10, max_length=10,
                        regex="^([12][0-9][0-9][0-9])-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$")
    tarjetas = ListField(EmbeddedDocumentField(Tarjeta))
    pedidos = ListField(ReferenceField(Pedido, reverse_delete_rule=4))

    def clean(self):
        self.validate(clean=False)
        err = "Formato del dni invalido!"
        if not self.dni[8].isalpha():
            raise(ValidationError(err))
        for i in range(8):
            if not self.dni[i].isnumeric():
                raise(ValidationError(err))
        letra = int(self.dni[0:8]) % 23
        if self.dni[8] != letras[letra]:
            raise(ValidationError(err))


def insertar():
    productos = [
        Producto(codigo_barras="1000000000009", nombre="Galletas",
                 categoria_principal=1, categorias_secundarias=[1, 2]),
        Producto(codigo_barras="2000000000008", nombre="Chocolate",
                 categoria_principal=2, categorias_secundarias=[2, 3, 4]),
        Producto(codigo_barras="3000000000007", nombre="Almendras",
                 categoria_principal=3, categorias_secundarias=[3]),
        Producto(codigo_barras="4006381333931", nombre="Leche",
                 categoria_principal=4, categorias_secundarias=[4, 5, 6, 7]),
    ]

    lineas = [
        Linea(num_items=1, precio_item=2.5, name="Galletas", total=2.5, ref=productos[0]),
        Linea(num_items=2, precio_item=3.5, name="Chocolate", total=7.0, ref=productos[1]),
        Linea(num_items=3, precio_item=4.5, name="Almendras", total=13.5, ref=productos[2]),
        Linea(num_items=4, precio_item=5.5, name="Leche", total=22, ref=productos[3])
    ]

    pedidos = [
        Pedido(total=9.5, fecha="2020,11,26", lineas=[lineas[0], lineas[1]]),
        Pedido(total=20.5, fecha="2020,11,26", lineas=[lineas[1], lineas[2]]),
        Pedido(total=35.5, fecha="2020,11,26", lineas=[lineas[2], lineas[3]]),
        Pedido(total=24.5, fecha="2020,11,26", lineas=[lineas[3], lineas[0]])
    ]

    tarjetas = [
        Tarjeta(nombre="Dale1", numero="1234567891234567", mes="01", año="02", ccv="034"),
        Tarjeta(nombre="Dale2", numero="1234567891234568", mes="02", año="03", ccv="044"),
        Tarjeta(nombre="Joesh1", numero="1234567891234569", mes="03", año="04", ccv="054"),
        Tarjeta(nombre="Joesh2", numero="1234567891234510", mes="04", año="05", ccv="064")
    ]
    personas = [
        Usuario(dni="65068806N", nombre="Dale", apellido1="Valencia",
                apellido2="Calicdan", f_nac="1993-04-02",
                tarjetas=[tarjetas[0], tarjetas[1]], pedidos=[pedidos[0], pedidos[1]]),
        Usuario(dni="65068807J", nombre="Josh", apellido1="Lopez",
                apellido2="Victor", f_nac="1990-02-16",
                tarjetas=[tarjetas[2], tarjetas[3]], pedidos=[pedidos[2], pedidos[3]])
    ]
    for producto in productos:
        producto.save()
    for pedido in pedidos:
        pedido.save()
    for persona in personas:
        persona.save()


insertar()
