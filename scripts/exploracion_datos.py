import sqlite3
import pandas as pd

# primero creo la conexión
db_path = "database.sqlite" 
conn = sqlite3.connect(db_path)

# para  ver las tablas que hay en ella
def listar_tablas(conn):
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql_query(query, conn)
    print("Tablas en la base de datos:")
    print(tables)
    return tables['name'].tolist()

# ahora miro el contenido de las tablas
def inspeccionar_tabla(conn, tabla):
    print(f"\nEstructura de la tabla '{tabla}':")
    query = f"PRAGMA table_info({tabla});"
    estructura = pd.read_sql_query(query, conn)
    print(estructura)
    return estructura

# saco los primeros registros
def resumen_estadistico(conn, tabla):
    print(f"\nPrimeros 10 registros de la tabla '{tabla}':")
    query = f"SELECT * FROM {tabla} LIMIT 5;"
    datos = pd.read_sql_query(query, conn)
    print(datos)

# aqui el resumen estadistico
    print(f"\nResumen estadistico de la tabla '{tabla}':")
    resumen = datos.describe(include='all')
    print(resumen)
    return resumen

# listo los resutlaados juntos
tablas = listar_tablas(conn)

for tabla in tablas:
    inspeccionar_tabla(conn, tabla)
    resumen_estadistico(conn, tabla)

#ccierro la conexión
conn.close()
