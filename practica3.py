import xml.sax

bibliotecas = dict()
class ManejadorCatalogo (xml.sax.ContentHandler):
    def __init__(self):
        self.ATRIBUTO=""
        self.LOCALIZACION=""
        self.CLASEVIAL=""
        self.NOMBREVIA=""
        self.NUM=""
        self.LOCALIDAD=""
        self.PROVINCIA=""
        self.CPOSTAL=""
        self.clave=""

    def startElement(self, etiqueta, atributos):
        if etiqueta=="atributo":
            self.ATRIBUTO=atributos["nombre"]
    def endElement(self, etiqueta):
        if etiqueta=="contenido":
            self.LOCALIZACION=list()
            self.LOCALIZACION.append(self.CLASEVIAL)
            self.LOCALIZACION.append(self.NOMBREVIA)
            self.LOCALIZACION.append(self.NUM)
            self.LOCALIZACION.append(self.LOCALIDAD)
            self.LOCALIZACION.append(self.PROVINCIA)
            self.LOCALIZACION.append(self.CPOSTAL)
            delimitador = " "
            bibliotecas[self.clave]["localizacion"]=delimitador.join(self.LOCALIZACION)
            self.LOCALIZACION=""
            self.CLASEVIAL=""
            self.NOMBREVIA=""
            self.NUM=""
            self.LOCALIDAD=""
            self.PROVINCIA=""
            self.CPOSTAL=""
            
        self.ATRIBUTO=""
    def characters(self, contenido):
        if self.ATRIBUTO=="ID-ENTIDAD":
            self.clave=contenido
            bibliotecas[self.clave]=dict()
            self.LOCALIZACION=list()
        elif self.ATRIBUTO=="NOMBRE":
            bibliotecas[self.clave]["nombre"]=contenido
        elif self.ATRIBUTO=="HORARIO":
            bibliotecas[self.clave]["horario"]=contenido
        elif self.ATRIBUTO=="EQUIPAMIENTO":
            bibliotecas[self.clave]["equipamiento"]=contenido
        elif self.ATRIBUTO=="TRANSPORTE":
            bibliotecas[self.clave]["transporte"]=contenido
        elif self.ATRIBUTO=="TELEFONO":
            bibliotecas[self.clave]["telefono"]=contenido
        elif self.ATRIBUTO=="EMAIL":
            bibliotecas[self.clave]["email"]=contenido
        elif self.ATRIBUTO=="NOMBRE-VIA":
            self.NOMBREVIA=contenido
        elif self.ATRIBUTO=="CLASE-VIAL":
            self.CLASEVIAL=contenido
        elif self.ATRIBUTO=="NUM":
            self.NUM=contenido
        elif self.ATRIBUTO=="LOCALIDAD":
            self.LOCALIDAD=contenido
        elif self.ATRIBUTO=="PROVINCIA":
            self.PROVINCIA=contenido
        elif self.ATRIBUTO=="CODIGO-POSTAL":
            self.CPOSTAL=contenido
            
parser=xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces,0)
Handler=ManejadorCatalogo()
parser.setContentHandler(Handler)
parser.parse("201747-0-bibliobuses-bibliotecas.xml")
for clave in bibliotecas:
    print (bibliotecas[clave]["nombre"])

entrada = input("Elige biblioteca: ")    
bib = {}
for clave in bibliotecas:
    if (bibliotecas[clave]["nombre"] == entrada):
        bib = bibliotecas.get(clave)

if not bool(bib):
    print("No existe esa biblioteca!")
else:
    print("\033[1mNombre de la biblioteca\033[0m")
    print(bib.get("nombre", "DESCONOCIDO"))
    print("\033[1mHorario\033[0m")
    print(bib.get("horario", "DESCONOCIDO"))
    print("\033[1mEquipamiento\033[0m")
    print(bib.get("equipamiento", "DESCONOCIDO"))
    print("\033[1mTransporte\033[0m")
    print(bib.get("transporte", "DESCONOCIDO"))
    print("\033[1mLocalización\033[0m")
    print(bib.get("localizacion", "DESCONOCIDO"))
    print("\033[1mTelefono\033[0m")
    print(bib.get("telefono", "DESCONOCIDO"))
    print("\033[1mEmail\033[0m")
    print(bib.get("email", "DESCONOCIDO"))