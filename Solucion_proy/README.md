El objetivo de la empresa BATSEJ OPEN FINANCE S.A es tener un procedimiento automatico que permita ver un resumen de los valores a cobrar a cada cliente activo en julio y agosto segun las condiciones que se tienen en el contrato, teniendo en cuenta que pueden variar y que son diferentes para cada uno e incluso cuando hay peticiones fallidas, se adiciona un descuento para algunos de ellos. 

## Se requiere:
- Python
- SQLite
- Libreria Pandas
- Libreria sqlite3
- Libreria smtplib
. Libreria email
- Servidor SMTP para Outlook

## Archivos en Solucion_proy
- `scripts`: Aquí se encuentran los codigos del proyecto, hay dos:
    - exploracion_datos.py: Donde se ve el contenido de la base database.sqlite
    - codigo.py: Aquí esta el codigo solucion, donde se ve filtro inicial, procedimineto para calcular las comisiones, procedimiento para crear el archivo de excel y tambien el envío del correo.
- `resultados_comisiones.xlsx`: Este es el archivo generado con el resumen de las comisiones.
- `database.sqlite`: Es la base de datos SQLite utilizada.

## Ejecución
1. Configurar credenciales en el script `codigo.py`.
2. Ejecutar el script:
   ```bash
   python codigo.py
