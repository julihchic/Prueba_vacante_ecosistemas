import sqlite3
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# primero establezo la conexion con la database
conn = sqlite3.connect('Solucion_proy\database.sqlite')
cursor = conn.cursor()

# fecha de inicio y de fin con mismo formato que me da la fecha de tabla apicall con el rango que me piden (jul-ago)
fecha_inicio = '2024-07-01 00:00:00'
fecha_fin = '2024-08-31 23:59:59'

# cfiltro las peticiones activas en las fechas indicadas
cursor.execute('''
SELECT commerce_id, COUNT(*) AS peticiones_exitosas, 
       SUM(CASE WHEN ask_status = 'Unsuccessful' THEN 1 ELSE 0 END) AS peticiones_fallidas
FROM apicall
WHERE date_api_call BETWEEN ? AND ?
GROUP BY commerce_id
''', (fecha_inicio, fecha_fin))

# resultadis
rows = cursor.fetchall()

# por si hay error, informar
if not rows:
    print("No se encontraron resultados en el rango de fechas indicado.")
else:
    # muestro resultados
    for row in rows:
        print(f'Comercio: {row[0]}, Peticiones Exitosas: {row[1]}, Peticiones Fallidas: {row[2]}')

        # logica para el calculo de las comisines
        commerce_id = row[0]
        peticiones_exitosas = row[1]
        peticiones_fallidas = row[2]
        
        # saco la info del comercio
        cursor.execute('''
        SELECT commerce_name, commerce_nit, commerce_email 
        FROM commerce 
        WHERE commerce_id = ?
        ''', (commerce_id,))
        commerce_info = cursor.fetchone()

        if commerce_info:
            commerce_name, commerce_nit, commerce_email = commerce_info
            print(f'Comercio: {commerce_name}, NIT: {commerce_nit}, Email: {commerce_email}')

            # creo condicionales segun se indicó en el pdf
            if commerce_name == "Innovexa Solutions":
                # comisión fija de $300 por petición buena + IVA
                comision_por_peticion = 300
                comision_total = comision_por_peticion * peticiones_exitosas
            elif commerce_name == "NexaTech Industries":
                # comisión variable según rango de peticiones
                if peticiones_exitosas <= 10000:
                    comision_por_peticion = 250
                elif peticiones_exitosas <= 20000:
                    comision_por_peticion = 200
                else:
                    comision_por_peticion = 170
                comision_total = comision_por_peticion * peticiones_exitosas
            elif commerce_name == "QuantumLeap Inc.":
                # comisión fija de $600 por petición buena + IVA
                comision_por_peticion = 600
                comision_total = comision_por_peticion * peticiones_exitosas
            elif commerce_name == "Zenith Corp.":
                # comisión variable según el rango de peticiones
                if peticiones_exitosas <= 22000:
                    comision_por_peticion = 250
                else:
                    comision_por_peticion = 130
                comision_total = comision_por_peticion * peticiones_exitosas
                # condicion de 5% de descuento (más de 6.000 peticiones fallidas)
                if peticiones_fallidas > 6000:
                    comision_total *= 0.95 
            elif commerce_name == "FusionWave Enterprises":
                # Comisión fija de $300 por petición buena + IVA
                comision_por_peticion = 300
                comision_total = comision_por_peticion * peticiones_exitosas
                # condición de 5% de descuento (entre 2.500 y 4.500 peticiones fallidas)
                if 2500 <= peticiones_fallidas <= 4500:
                    comision_total *= 0.95 
                # condicion de 8% de descuento (más de 4.500 peticiones fallidas)
                elif peticiones_fallidas > 4500:
                    comision_total *= 0.92
            else:
                comision_total = 0

            # Ahora se calcula el IVA de 19%
            iva = comision_total * 0.19
            total_con_iva = comision_total + iva

            # Muestro resultados
            print(f'Comisión total: {comision_total} COP')
            print(f'IVA: {iva} COP')
            print(f'Total con IVA: {total_con_iva} COP\n')

            # Guardo resultados en un DF
            data = {
                'Fecha': [datetime.now().strftime('%Y-%m-%d')],
                'Mes': [datetime.now().strftime('%B')],
                'Nombre': [commerce_name],
                'Nit': [commerce_nit],
                'Valor_Comision': [comision_total],
                'Valor_Iva': [iva],
                'Valor_Total': [total_con_iva],
                'Correo': [commerce_email]
            }

            df = pd.DataFrame(data)

            # guardo el DF en un excel
            df.to_excel('resultados_comisiones.xlsx', index=False)

            print(f'Los resultados han sido guardados en el archivo "resultados_comisiones.xlsx".\n')


comercios = [
    {"Fecha_Mes": "2024-10", "Nombre": "Zenith Corp.", "Nit": "28960112", "Valor_comision": 6285162.0, "Valor_iva": 1194180.78, "Valor_total": 7479342.78, "Correo": "zenithcorp.@gemaily.net"},
    {"Fecha_Mes": "2024-11", "Nombre": "FusionWave Enterprises", "Nit": "919341007", "Valor_comision": 14048400.0, "Valor_iva": 2669196.0, "Valor_total": 16717596.0, "Correo": "fusionwaveenterprises@microfitsof.com"},
    {"Fecha_Mes": "2024-12", "Nombre": "Innovexa Solutions", "Nit": "445470636", "Valor_comision": 15205200.0, "Valor_iva": 2888988.0, "Valor_total": 18094188.0, "Correo": "innovexasolutions@microfitsof.com"},
    {"Fecha_Mes": "2024-07", "Nombre": "QuantumLeap Inc.", "Nit": "198818316", "Valor_comision": 30501000.0, "Valor_iva": 5795190.0, "Valor_total": 36296190.0, "Correo": "quantumleapinc.@gemaily.net"},
    {"Fecha_Mes": "2024-09", "Nombre": "NexaTech Industries", "Nit": "452680670", "Valor_comision": 8636680.0, "Valor_iva": 1640969.2, "Valor_total": 10277649.2, "Correo": "nexatechindustries@gemaily.net"}
]

# creo un DF para la tabla
df_comercios = pd.DataFrame(comercios)

# tabla htnl
tabla_html = df_comercios.to_html(index=False, header=True)

# caracteristicas del corre0
envia_email = "bot@dominio.com"
recibe_email = "ejecutor@dominio.com"  
smtp_server = "smtp.outlook.com"
smtp_port = 587
clave = "bot_clave"  

# cabeceras del correo
mensaje = MIMEMultipart()
mensaje["From"] = envia_email
mensaje["To"] = recibe_email
mensaje["Subject"] = "Comisiones y Resultados del Mes"

# contenido del mensaje con la tabla
cuerpo_msj = f"""
A quien pueda interesar,

Adjunto los resultados de las comisiones y los valores asociados para el mes de julio y agosto de 2024. Les comparto un resumen en la siguiente tabla.

{tabla_html}

Saludos,
BATSEJ OPEN FINANCE S.A
"""
mensaje.attach(MIMEText(cuerpo_msj, "html", _charset="utf-8")) 

# adjunto el excel en el correo
archivo_excel = "resultados_comisiones.xlsx"
with open(archivo_excel, "rb") as attachment:
    part = MIMEApplication(attachment.read(), Name=archivo_excel)
    part['Content-Disposition'] = f'attachment; filename="{archivo_excel}"'
    mensaje.attach(part)

# lo envío
try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(envia_email, clave)
        server.sendmail(envia_email, recibe_email, mensaje.as_string())
    print("Correo enviado correctamente.")
except Exception as e:
    print(f"Error al enviar el correo: {e}")

# cierro la conexion a database
cursor.close()
conn.close()

print("Proceso finalizado")


