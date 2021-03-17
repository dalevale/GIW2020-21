import sqlite3
conn=sqlite3.connect("baloncesto.sqlite3")
cur=conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS equipos(registro INTEGER PRIMARY KEY, nombre TEXT, nombre_entrenador TEXT, nombre_cancha TEXT, poblacion TEXT, anio_fundacion INTEGER, anotacion TEXT)''')
cur.executemany("INSERT INTO equipos VALUES (?,?,?,?,?,?,?)", [
                (1, 'Winterthur F.C. Barcelona', 'Dusko Ivanovic', 'Palau Blaugrana', 'BARCELONA', 1926, 'Ganador de copa de Europa'),
                (2, 'Real Madrid', 'Joan Plaza', 'Palacio de Vistalegre', 'MADRID', 1932, 'Ganador de copa de Europa y varias ligas'),
                (3, 'Club Baloncesto Estudiantes', 'Pedro Martínez', 'Madrid Arena', 'MADRID', 1948, ''),
                (4, 'Unicaja Málaga', 'Sergio Scariolo', 'Palacio de Deportes', 'MALAGA', 1992, 'Último ganador de la liga ACB 2006'),
                (5, 'Caja San Fernando', 'Manel Comas', 'Palacio municipal de los deportes San Pablo', 'SEVILLA', 1987, ''),
                (6, 'TAU Cerámica', 'Velimir Perasovic', 'Fernando Buesa Arena', 'VITORIA', 1959, ''),
                (7, 'Joventut de Badalona', 'Aíto García Reneses', 'Pabellón Olímpico de Badalona', 'BADALONA', 1930, '')])
print(cur.rowcount)
cur.execute('''CREATE TABLE IF NOT EXISTS partidos(registro INTEGER PRIMARY KEY, id_equipo1 INTEGER,
id_equipo2 INTEGER, resultado_equipo1 INTEGER, resultado_equipo2 INTEGER)''')
cur.executemany("INSERT INTO partidos VALUES (?,?,?,?,?)",[
                (1, 1, 7, 100, 99),
                (2, 1, 3, 66, 45),
                (3, 2, 3, 68, 92),
                (4, 7, 1, 50,60),
                (5, 5, 1, 76, 45),
                (6, 2, 1, 99, 98),
                (7, 6, 1, 101, 103),
                (8, 6, 2, 80, 85),
                (9, 3, 5, 80, 80),
                (10, 3, 1, 57, 65),
                (11, 3, 2, 67, 58)])
print (cur.rowcount)
cur.close()
conn.commit()

import sqlite3

def numeroEquipos():
    conn=sqlite3.connect("baloncesto.sqlite3")
    cur=conn.cursor()
    cur.execute("SELECT poblacion, COUNT(poblacion) FROM equipos GROUP BY poblacion;")
    for fila in cur.fetchall():
        print("Población ", fila[0])
        print("Numero Equipos", fila[1])
    cur.close()

def resultados():
    conn=sqlite3.connect("baloncesto.sqlite3")
    cur=conn.cursor()
    cur.execute("SELECT eq1.nombre, partidos.resultado_equipo1, eq2.nombre, partidos.resultado_equipo2 FROM partidos INNER JOIN equipos AS eq1 ON partidos.id_equipo1=eq1.registro INNER JOIN equipos AS eq2 ON partidos.id_equipo2=eq2.registro ORDER BY eq1.nombre;")
    print(cur.rowcount)
    for fila in cur.fetchall():
        print(fila[0], " contra ", fila[2])
        print("Resultado:", fila[1], "  ", fila[3])
    cur.close()
    
def partidosJugados():
    conn=sqlite3.connect("baloncesto.sqlite3")
    cur=conn.cursor()
    cur.execute("SELECT e.nombre, COUNT(p.id_equipo1) FROM partidos AS p JOIN equipos AS e ON e.registro=p.id_equipo1 GROUP BY p.id_equipo1 ORDER BY COUNT(*) DESC;")

    for fila in cur.fetchall():
        print("Equipo ", fila[0])
        print("Numero de partidos Jugados", fila[1])
    cur.close()

def mediaResultados():
    conn=sqlite3.connect("baloncesto.sqlite3")
    cur=conn.cursor()
    cur.execute("SELECT e.nombre, AVG(res) FROM"+
                "(SELECT e.registro AS eq, p.resultado_equipo1 AS res FROM partidos p JOIN equipos e ON e.registro=p.id_equipo1 " +
                "UNION SELECT e.registro AS eq, p.resultado_equipo2 AS res FROM partidos p JOIN equipos e ON e.registro=p.id_equipo2) " +
                "JOIN equipos e ON eq=e.registro GROUP BY eq ORDER BY AVG(res) DESC;")
    for fila in cur.fetchall():
        print ("Nombre: ", fila[0])
        print ("Media: ", fila[1])
    cur.close()
    
def ningunPartido():
    conn=sqlite3.connect("baloncesto.sqlite3")
    cur=conn.cursor()
    cur.execute("SELECT nombre, nombre_entrenador, nombre_cancha, poblacion, anio_fundacion FROM equipos WHERE equipos.registro NOT IN (SELECT id_equipo1 FROM partidos GROUP BY id_equipo1) AND equipos.registro NOT IN (SELECT id_equipo2 FROM partidos GROUP BY id_equipo2);")

    for fila in cur.fetchall():
        print("Equipo ", fila[0])
        print("Entrenador ", fila[1])
        print("Cancha ", fila[2])
        print("Poblacion ", fila[3])
        print("Año Fundación ", fila[4])
    cur.close()

def maximaDiferencia():
    conn=sqlite3.connect("baloncesto.sqlite3")
    cur=conn.cursor()
    cur.execute("SELECT e1.nombre, e2.nombre, MAX(ABS(DIFFERENCE(p.resultado_equipo1, p.resultado_equipo2))) FROM equipos AS e1 JOIN partidos p ON e1.registro=p.id_equipo1 JOIN equipos AS e2 ON e2.registro=p.id_equipo2 GROUP")

    for fila in cur.fetchall():
        print("Equipo ", fila[0])
    cur.close()
    
#numeroEquipos()
#resultados()
partidosJugados()
#mediaResultados()
#maximaDiferencia()
#ningunPartido()