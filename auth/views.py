########### Imports Flask & Python ##########

import pandas as pd
from openpyxl import Workbook

from werkzeug.utils import secure_filename

#from xlsx2pdf import converter

from flask import (redirect, render_template, request, 
                Blueprint, url_for)
from werkzeug.security import generate_password_hash

from flask_login import login_user, login_required, logout_user
from flask_login import current_user
from flask import flash

from db.db_connection import get_connection

from flask_sqlalchemy import SQLAlchemy

from .models import  get_user_by_username, get_user_by_username_and_password
from flask import jsonify
########### Imports Forms ##########
from .forms import ProductoForm, AreaForm, SolicitudForm, ReportForm, LlenarTablaForm, AceptadasForm,ProductoeditarForm,AreaeditarForm,LlenarTablaeditarForm


from xhtml2pdf import pisa
auth_blueprint = Blueprint('auth', __name__)

############ Rutas Login ############


  





@auth_blueprint.route('/producto', methods=['GET', 'POST'])
@login_required
def producto():
    form = ProductoForm()

    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "SELECT ID, nombre FROM Proveedores"
        cursor.execute(sql)
        areas = cursor.fetchall()
    form.area.choices = [(g['ID'], g['nombre']) for g in areas]
    if form.validate_on_submit():
        # Aquí puedes guardar los datos del formulario en la base de datos
        nombre = form.nombre.data
        descripcion = form.descripcion.data
        
        cantidad_disponible = form.cantidad_disponible.data
        fecha = form.fecha.data
        lote = form.lote.data
        area = form.area.data


        #conn = get_connection()
        #with conn.cursor() as cursor:
        # Reemplaza 'area' con el campo adecuado para filtrar por el ID del proveedor
        #    sql = f"SELECT nombre FROM Proveedores WHERE ID = {area}"
         #   cursor.execute(sql)
          #  user_details = cursor.fetchone()

        # Combina los campos de nombre, apellido_paterno y apellido_materno para obtener el nombre completo del usuario
        #usuario_nombre_completo = user_details['nombre']


        conn = get_connection()
        with conn.cursor() as cursor:
            sql = "INSERT INTO Material (nombre, descripcion,cantidad_disponible, fecha_registro ,lote,proveedor_id) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, ( nombre, descripcion, cantidad_disponible, fecha,lote,area ))
            conn.commit()
        # Realiza las operaciones necesarias para guardar los datos en la base de datos

        return redirect(url_for('home.User'))

    return render_template('admin/producto.html', form=form)


@auth_blueprint.route('/producto/editar/<int:producto_id>', methods=['GET', 'POST'])
@login_required
def editar_producto(producto_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM Material WHERE ID = %s"
        cursor.execute(sql, (producto_id,))
        producto = cursor.fetchone()

        sql = "SELECT ID, nombre FROM Proveedores"
        cursor.execute(sql)
        proveedores = cursor.fetchall()

    form = ProductoeditarForm()
    form.area.choices = [(g['ID'], g['nombre']) for g in proveedores]

    if request.method == 'POST':
        if form.validate_on_submit():
            nombre = form.nombre.data
            descripcion = form.descripcion.data
            cantidad_disponible = form.cantidad_disponible.data
            lote = form.lote.data
            area = form.area.data

            conn = get_connection()
            with conn.cursor() as cursor:
                sql = "UPDATE Material SET nombre = %s, descripcion = %s, cantidad_disponible = %s, lote = %s, proveedor_id = %s WHERE ID = %s"
                cursor.execute(sql, (nombre, descripcion, cantidad_disponible, lote, area, producto_id))
                conn.commit()

            return redirect(url_for('home.User'))

    form.nombre.data = producto['nombre']
    form.descripcion.data = producto['descripcion']
    form.cantidad_disponible.data = producto['cantidad_disponible']
    form.lote.data = producto['lote']
    form.area.data = producto['proveedor_id']

    return render_template('admin/editar_producto.html', form=form, producto=producto)




#@auth_blueprint.route('/register')
#def register():
#
 #   form = RegisterForm()

  #  return render_template('auth/register.html', form=form)

@auth_blueprint.route('/inventario')
@login_required
def inventario():
    # Crear un cursor
    conn = get_connection()
    with conn.cursor() as cursor:
        # Ejecutar una consulta para seleccionar todos los datos de la vista
        sql = "SELECT * FROM Material"
        cursor.execute(sql)

        # Recuperar los resultados
        materiales = cursor.fetchall()

    # Crear una lista para almacenar los detalles de los materiales, incluido el nombre del proveedor
    materiales_con_detalles = []

    # Recorrer cada material y obtener el nombre del proveedor correspondiente
    for material in materiales:
        proveedor_id = material['proveedor_id']

        with conn.cursor() as cursor:
            # Obtener el nombre del proveedor usando el proveedor_id
            sql = f"SELECT nombre FROM Proveedores WHERE ID = {proveedor_id}"
            cursor.execute(sql)
            proveedor = cursor.fetchone()

        # Crear un nuevo diccionario con los detalles del material, incluido el nombre del proveedor
        material_con_detalles = {
            'ID': material['ID'],
            'nombre': material['nombre'],
            'descripcion': material['descripcion'],
            'cantidad': material['cantidad_disponible'],
            'lote' : material['lote'],
            'fecha' : material['fecha_registro'],
            'proveedor': proveedor['nombre'] if proveedor else 'Proveedor no encontrado'
        }

        # Agregar el diccionario a la lista de materiales con detalles
        materiales_con_detalles.append(material_con_detalles)

    # Cerrar la conexión a la base de datos
    conn.close()

    # Renderizar la plantilla HTML con los datos de los materiales y sus detalles
    return render_template('auth/inventario.html', materiales=materiales_con_detalles)


@auth_blueprint.route('/inventario/buscar', methods=['GET', 'POST'])
@login_required
def inventariobuscar():
    # Crear un cursor
    conn = get_connection()
    with conn.cursor() as cursor:
        if request.method == 'POST':
            # Obtener el criterio de búsqueda del formulario
            search_term = request.form.get('search_term')

            # Construir la consulta SQL con el criterio de búsqueda
            sql = "SELECT * FROM Material WHERE nombre LIKE %s OR descripcion LIKE %s"
            
            # Ejecutar la consulta SQL con el parámetro de búsqueda
            cursor.execute(sql, (f"%{search_term}%", f"%{search_term}%"))
        else:
            # Si no se envió una solicitud POST, obtener todos los datos de la tabla Material
            sql = "SELECT * FROM Material"
            cursor.execute(sql)
            
        # Recuperar los resultados
        materiales = cursor.fetchall()

        # Crear una lista para almacenar los detalles de los materiales, incluido el nombre del proveedor
        materiales_con_detalles = []

        # Recorrer cada material y obtener el nombre del proveedor correspondiente
        for material in materiales:
            proveedor_id = material['proveedor_id']

            with conn.cursor() as cursor:
                # Obtener el nombre del proveedor usando el proveedor_id
                sql = f"SELECT nombre FROM Proveedores WHERE ID = {proveedor_id}"
                cursor.execute(sql)
                proveedor = cursor.fetchone()

            # Crear un nuevo diccionario con los detalles del material, incluido el nombre del proveedor
            material_con_detalles = {
                'ID': material['ID'],
                'nombre': material['nombre'],
                'descripcion': material['descripcion'],
                'cantidad': material['cantidad_disponible'],
                'lote': material['lote'],
                'fecha': material['fecha_registro'],
                'proveedor': proveedor['nombre'] if proveedor else 'Proveedor no encontrado'
            }

            # Agregar el diccionario a la lista de materiales con detalles
            materiales_con_detalles.append(material_con_detalles)

    # Cerrar la conexión a la base de datos
    conn.close()

    # Renderizar la plantilla HTML con los datos de los materiales y sus detalles
    return render_template('auth/inventario.html', materiales=materiales_con_detalles)


@auth_blueprint.route('/borrar_material/<int:material_id>', methods=['POST'])
@login_required
def borrar_material(material_id):
    # Realiza las operaciones necesarias para borrar el material con el ID especificado
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "DELETE FROM Material WHERE ID = %s"
        cursor.execute(sql, (material_id,))
        conn.commit()

    # Redirecciona a la página de inventario después de borrar el material
    return redirect(url_for('auth.inventario'))



@auth_blueprint.route('/areas', methods=['GET', 'POST'])
@login_required
def areas():
    form = AreaForm()
    if form.validate_on_submit():
        # Aquí puedes guardar los datos del formulario en la base de datos
        nombre = form.nombre.data
        descripcion = form.descripcion.data
        password = form.password.data
        email = form.email.data

        
        conn = get_connection()
        with conn.cursor() as cursor:
            sql = "INSERT INTO Area (nombre, descripcion,clave,correo) VALUES (%s, %s,%s,%s)"
            cursor.execute(sql, (nombre, descripcion,password,email))
            conn.commit()
        # Realiza las operaciones necesarias para guardar los datos en la base de datos

        return redirect(url_for('home.User'))

    return render_template('admin/areas.html', form=form)

@auth_blueprint.route('/vista_de_area', methods=['GET'])
@login_required
def vista_de_area():
    # Crear un cursor
    conn = get_connection()
    with conn.cursor() as cursor:
        # Ejecutar una consulta para seleccionar todos los datos de la vista
        sql = "SELECT * FROM Area"
        cursor.execute(sql)

        # Recuperar los resultados
        usuarios = cursor.fetchall()

        # Cerrar el cursor
        cursor.close()

        # Renderizar la plantilla HTML con los datos de los usuarios
        return render_template('auth/vista_de_area.html', usuarios=usuarios)



@auth_blueprint.route('/areas/borrar/<int:area_id>', methods=['POST'])
@login_required
def borrar_area(area_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "DELETE FROM Area WHERE ID = %s"
        cursor.execute(sql, (area_id,))
        conn.commit()
    return redirect(url_for('home.User'))


@auth_blueprint.route('/areasbuscar',  methods=['GET', 'POST'])
@login_required
def areasbuscar():
    # Crear un cursor
    conn = get_connection()
    with conn.cursor() as cursor:
        if request.method == 'POST':
            # Obtener el criterio de búsqueda del formulario
            search_term = request.form.get('search_term')

            # Construir la consulta SQL con el criterio de búsqueda
            sql = "SELECT * FROM Area WHERE nombre LIKE %s OR descripcion LIKE %s"
            
            # Ejecutar la consulta SQL con el parámetro de búsqueda
            cursor.execute(sql, (f"%{search_term}%", f"%{search_term}%"))

            # Recuperar los resultados
            usuarios = cursor.fetchall()

            # Cerrar el cursor
            cursor.close()

            # Renderizar la plantilla HTML con los datos de los usuarios
            return render_template('auth/vista_de_area.html', usuarios=usuarios)

        else:
            # Si no se envió una solicitud POST, redirigir a la página 'vista_de_area' con GET
            return redirect(url_for('auth.vista_de_area'))


@auth_blueprint.route('/areas/editar/<int:area_id>', methods=['GET', 'POST'])
@login_required
def editar_area(area_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        # Obtener los datos del área a editar
        sql = "SELECT * FROM Area WHERE ID = %s"
        cursor.execute(sql, (area_id,))
        area = cursor.fetchone()

    form =  AreaeditarForm()
    if request.method == 'POST' and form.validate_on_submit():
        nombre = form.nombre.data
        descripcion = form.descripcion.data

        conn = get_connection()
        with conn.cursor() as cursor:
            sql = "UPDATE Area SET nombre = %s, descripcion = %s WHERE ID = %s"
            cursor.execute(sql, (nombre, descripcion, area_id))
            conn.commit()

        return redirect(url_for('home.User'))

    # Rellenar el formulario con los datos del área a editar
    form.nombre.data = area['nombre']
    form.descripcion.data = area['descripcion']

    return render_template('admin/editar_area.html', form=form, area=area)



@auth_blueprint.route('/usuarios')
@login_required
def usuarios():
    # Crear un cursor
    conn = get_connection()
    with conn.cursor() as cursor:
        # Ejecutar una consulta para seleccionar todos los datos de la vista
        sql = "SELECT * FROM Usuario"
        cursor.execute(sql)

        # Recuperar los resultados
        usuarios = cursor.fetchall()

        # Cerrar el cursor
        cursor.close()

        # Renderizar la plantilla HTML con los datos de los usuarios
        return render_template('auth/usuarios.html', usuarios=usuarios)


@auth_blueprint.route('/usuarios/buscar',  methods=['GET', 'POST'])
@login_required
def buscar_usuarios():
    # Crear un cursor
    conn = get_connection()
    with conn.cursor() as cursor:
        if request.method == 'POST':
            # Obtener el criterio de búsqueda del formulario
            search_term = request.form.get('search_term')

            # Construir la consulta SQL con el criterio de búsqueda
            sql = "SELECT * FROM Usuario WHERE nombre LIKE %s OR apellido_paterno  LIKE %s"
            
            # Ejecutar la consulta SQL con el parámetro de búsqueda
            cursor.execute(sql, (f"%{search_term}%", f"%{search_term}%"))

            # Recuperar los resultados
            usuarios = cursor.fetchall()

            # Cerrar el cursor
            cursor.close()

            # Renderizar la plantilla HTML con los datos de los usuarios
            return render_template('auth/usuarios.html', usuarios=usuarios)

        else:
            # Si no se envió una solicitud POST, redirigir a la página 'vista_de_area' con GET
            return redirect(url_for('auth.usuarios'))


from datetime import date
from flask import request, render_template, session

# Definir la clase Material fuera de la función obtener_materiales_disponibles()
class Material:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

def obtener_materiales_disponibles():
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM Material"
        cursor.execute(sql)
        materiales = cursor.fetchall()

        if materiales:
            # Convertir los resultados en objetos Material
            materiales_obj = [Material(material['ID'], material['nombre']) for material in materiales]
            return materiales_obj
        else:
            # Manejar caso de que no haya materiales disponibles
            return []

# En views.py

from flask import request


from flask_login import login_required
from io import BytesIO
from datetime import date
import pdfkit


from fpdf import FPDF
import pandas as pd




from fpdf import FPDF
import pandas as pd
import io

# Resto del código...
from datetime import datetime

# Resto del código...
from datetime import datetime
import email

import pandas as pd
from fpdf import FPDF
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import render_template, send_file, make_response

import pdfkit
from io import BytesIO
from xhtml2pdf import pisa
from email.mime.base import MIMEBase
from email import encoders
# Resto del código de la función...
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from flask import make_response
import imaplib

import imaplib
import datetime
from dateutil.parser import parse

import imaplib
import email
from datetime import datetime, timedelta
import email
import imaplib
from datetime import datetime, timedelta

import email
import imaplib
from datetime import datetime, timedelta
import os
import email
import imaplib
from datetime import datetime, timedelta

def obtener_ruta_adjunto(mensaje, directorio_destino):
    nombre_archivo = mensaje.get_filename()

    if nombre_archivo:
        ruta_destino = os.path.join(directorio_destino, nombre_archivo)
        contador = 1
        while os.path.exists(ruta_destino):
            nombre_archivo_nuevo = f"{nombre_archivo}_{contador}"
            ruta_destino = os.path.join(directorio_destino, nombre_archivo_nuevo)
            contador += 1

        return ruta_destino

    return None

import os
import email
import imaplib
from datetime import datetime, timedelta

# ... Las demás funciones se mantienen igual ...
def obtener_url_adjunto(mensaje):
    """
    Obtener la URL del mensaje en Gmail para acceder al adjunto.
    """
    # Obtener el ID único del mensaje en Gmail
    mensaje_id = mensaje.get('Message-ID')

    if mensaje_id:
        # Generar la URL del mensaje en Gmail
        url_adjunto = f"https://mail.google.com/mail/u/0/#inbox/{mensaje_id}"
        return url_adjunto

    return None






# ... Las demás funciones se mantienen igual ...



        # ... Código anterior ...

       # ... Código anterior ...
def obtener_mensajes_bandeja_entrada(usuario_correo, contrasena):
    # Conectar al servidor IMAP de Gmail
    imap_server = imaplib.IMAP4_SSL("imap.gmail.com", 993)

    try:
        # Iniciar sesión en la cuenta de correo
        imap_server.login(usuario_correo, contrasena)

        # Seleccionar la bandeja de entrada
        imap_server.select("INBOX")

        # Obtener la fecha actual
        fecha_actual = datetime.now()

        # Calcular la fecha hace 7 días
        fecha_hace_siete_dias = fecha_actual - timedelta(days=4)

        # Convertir las fechas a formato string en el formato correcto para el comando SEARCH
        fecha_desde = fecha_hace_siete_dias.strftime("%d-%b-%Y")  # Ejemplo: "01-Jul-2023"
        fecha_actual_str = fecha_actual.strftime("%d-%b-%Y")  # Ejemplo: "08-Jul-2023"

        # Filtrar mensajes desde la fecha hace 7 días hasta la fecha actual
        status, mensajes = imap_server.search(None, f"SINCE {fecha_desde} BEFORE {fecha_actual_str}")

        lista_mensajes = []
        

        # ... Código anterior ...

        if status == "OK":
            # Iterar sobre los IDs de los mensajes
            for mensaje_id in mensajes[0].split():
                # Obtener el contenido del mensaje y otros atributos relevantes
                status, mensaje_data = imap_server.fetch(mensaje_id, "(RFC822)")

                if status == "OK":
                    # Parsear el mensaje utilizando la librería email
                    mensaje = email.message_from_bytes(mensaje_data[0][1])

                    # Obtener los atributos relevantes del mensaje
                    mensaje_info = {
                        "subject": mensaje["subject"],
                        "from": mensaje["from"],
                        "to": mensaje["to"],
                        "date": mensaje["date"],
                        "content_type": mensaje.get_content_type(),
                        "id": mensaje_id,
                    }
                    print(mensaje_info)

                    # Verificar si el mensaje tiene adjunto
                    if mensaje.get_content_maintype() == "multipart":
                        for part in mensaje.walk():
                            content_disposition = str(part.get("Content-Disposition"))

                            # Si es un archivo adjunto, obtener la URL del mensaje en Gmail
                            if "attachment" in content_disposition:
                                url_adjunto = obtener_url_adjunto(mensaje)
                                if url_adjunto:
                                    mensaje_info["url_adjunto"] = url_adjunto
                                    break  # Detener el bucle para evitar obtener múltiples URLs de adjuntos

                    lista_mensajes.append(mensaje_info)
                    # Después de crear la lista lista_mensajes
                    

                    # Marcar el mensaje como leído (visto)
                    imap_server.store(mensaje_id, "+FLAGS", "\\Seen")
        lista_mensajes = sorted(lista_mensajes, key=lambda x: x["date"], reverse=True)
            

# ... Código posterior ...


    except Exception as e:
        print("Error:", e)
        # Manejar el error o propagarlo según sea necesario

    finally:
        # Cerrar la conexión con el servidor IMAP
        try:
            imap_server.logout()
        except Exception as e:
            print("Error al cerrar la conexión:", e)

    return lista_mensajes

# Resto del código...


def obtener_cuerpo_mensaje(mensaje):
    """
    Obtener el cuerpo del mensaje.
    Si el mensaje es multipart, identifica la parte que contiene el cuerpo del mensaje.
    """
    if mensaje.is_multipart():
        for part in mensaje.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            # Si el contenido es texto y no es un archivo adjunto, es el cuerpo del mensaje
            if "text/plain" in content_type and "attachment" not in content_disposition:
                return part.get_payload()
    else:
        return mensaje.get_payload()

    return None


# Resto del código...









@auth_blueprint.route('/ver_correo')
def ver_correo():
    usuario_correo = "@gmail.com"  # Reemplaza con la dirección de correo electrónico de gestionde recursos y materiales
    contrasena = "msfechovcuaflztf"  # Reemplaza con tu contraseña
    mensajes = obtener_mensajes_bandeja_entrada(usuario_correo, contrasena)
    return render_template('auth/bandeja_de_entrada.html', mensajes=mensajes)




def descargarpdf(pdf_data):
    print('inicio de descarga')
    #print(pdf_data.read())
    response = make_response(pdf_data.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={"informe.pdf"}'

    return response


def obtener_credenciales_correo():
    conn = get_connection()
    with conn.cursor() as cursor:
        # Ejecutar una consulta para seleccionar todos los datos de la vista
     
        sql = f"SELECT correo, clave, nombre FROM Area WHERE id = {current_user.area}"
        cursor.execute(sql)

        # Recuperar los resultados
        result = cursor.fetchone()
        return result



def enviar_correo_con_adjunto(pdf_data):
    credenciales = obtener_credenciales_correo()
    # Configuración del servidor SMTP y credenciales de correo electrónico
    smtp_server = 'smtp.gmail.com'  # Reemplaza con el servidor SMTP que corresponda
    smtp_port = 587  # Puerto SMTP para TLS
    correo_emisor = credenciales['correo']  #  dirección de correo electrónico
    correo_receptor = '@gmail.com'  # Reemplaza con la dirección de correo electrónico de gestionde recursos y materiales
    contraseña = credenciales['clave']  # la contraseña de tu cuenta de correo

    # Crear el objeto del mensaje
    msg = MIMEMultipart()
    msg['From'] = correo_emisor
    msg['To'] = correo_receptor
    msg['Subject'] = 'Informe de solicitud'

    # Adjuntar el archivo PDF al mensaje
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(pdf_data.getvalue())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename=informe.pdf')
    msg.attach(part)

    # Conectar al servidor SMTP y enviar el correo
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(correo_emisor, contraseña)
            server.sendmail(correo_emisor, correo_receptor, msg.as_string().encode('ascii', 'ignore'))
        print("Correo enviado correctamente.")
    except Exception as e:
        flash(f"Error al enviar el correo: {str(e)}", "error")  # Mensaje de error

        return redirect(url_for('auth.error_de_red'))


def render_template(template_name, **kwargs):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_name)
    return template.render(kwargs)        

def generar_pdf_y_enviar_correo(numero_peticion, descripcion):
    # Resto del código para obtener los datos de la base de datos y generar el DataFrame df
    conn = get_connection()
    with conn.cursor() as cursor:
    
        sql = "SELECT numero_requisicion, descripcion, usuario_solicitante, area_solicitante, fecha_solicitud, material, unidad_de_medida, cantidad FROM Solicitud WHERE numero_requisicion = %s AND descripcion = %s"
        cursor.execute(sql, (numero_peticion, descripcion))
        solicitud_data = cursor.fetchall()
        print(solicitud_data)

    if len(solicitud_data) == 0:
        flash('¡No se encontraron coincidencias en la base de datos!', 'error')
        return redirect(url_for('auth.error_de_red'))

    # Obtener los datos adicionales de la consulta y almacenarlos en variables
    credenciales = obtener_credenciales_correo()
    usuario_solicitante = []
    area_solicitante = credenciales['nombre']
    fecha = []
    material = []
    unidad_de_medida = []
    cantidad = []

    for solicitud in solicitud_data:
        usuario_solicitante.append(solicitud['usuario_solicitante'])
        fecha.append(solicitud['fecha_solicitud'])
        material.append(solicitud['material'])
        unidad_de_medida.append(solicitud['unidad_de_medida'])
        cantidad.append(solicitud['cantidad'])

    # Consultar en BD por usuario_solicitante para obtener los nombres completos de los usuarios
    conn = get_connection()
    with conn.cursor() as cursor:
        usuarios_nombres_completos = []
        for user_id in usuario_solicitante:
            sql = f"SELECT nombre, apellido_paterno, apellido_materno FROM Usuario WHERE ID = {user_id}"
            cursor.execute(sql)
            user_details = cursor.fetchone()
            nombre_completo = f"{user_details['nombre']} {user_details['apellido_paterno']} {user_details['apellido_materno']}"
            usuarios_nombres_completos.append(nombre_completo)

    # Generar el DataFrame
    # Asegurar que todas las listas tengan la misma longitud
    num_rows = len(solicitud_data)
    #area_solicitante = solicitud_data[0]['area_solicitante']
    fecha = [peticion['fecha_solicitud'] for peticion in solicitud_data]
    material = [peticion['material'] for peticion in solicitud_data]
    unidad_de_medida = [peticion['unidad_de_medida'] for peticion in solicitud_data]
    cantidad = [peticion['cantidad'] for peticion in solicitud_data]
    numero_coincidencias = len(solicitud_data)


    # Crear el DataFrame con las listas actualizadas
    data = {
        'Número de Petición': [numero_peticion] * num_rows,
        'Número': [numero_coincidencias] * num_rows,
        'Descripción': [descripcion] * num_rows,
        'Nombre del Solicitante': usuarios_nombres_completos,
        'Área Solicitante': [area_solicitante] * num_rows,
        'Fecha': fecha,
        'Material': material,
        'Unidad': unidad_de_medida,
        'Cantidad': cantidad
        # Agrega aquí los demás campos que desees mostrar en el PDF
    }
    df = pd.DataFrame(data)

    
    print('data:', df)



    

    # Renderizar el archivo HTML utilizando Jinja y almacenar el resultado en una variable
    html = render_template('informe_template.html',  data=df)

    # Agregar declaración de codificación UTF-8 al inicio del archivo HTML
    html = f"<!DOCTYPE html><html><head><meta charset='UTF-8'></head><body>{html}</body></html>"
    
    

    # Generar el PDF utilizando pdfkit con las opciones configuradas
    
    # Generar el PDF utilizando pdfkit
    pdf_bytes = pdfkit.from_string(html, False)

    # Enviar el PDF por correo electrónico
    pdf_data = io.BytesIO(pdf_bytes)
    enviar_correo_con_adjunto(pdf_data)
    descargarpdf(pdf_data)
    # Redirigir al usuario a la página de solicitud exitosa después de generar el PDF
    return "El PDF ha sido generado y enviado correctamente."


def get_user_by_username(username):
    # Consultar en BD por username
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = f"SELECT ID, nombre, tipo, area FROM Usuario WHERE nombre = '{username}'"
        cursor.execute(sql)
        user = cursor.fetchone()
        if user:
            return User(user['ID'], user['nombre'], user['tipo'], user['area'])
        else:
            return None


@auth_blueprint.route('/crear_solicitud', methods=['GET', 'POST'])
@login_required
def crear_solicitud():
    form = SolicitudForm()

    # Realiza una consulta a la base de datos para obtener los detalles completos del usuario
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = f"SELECT nombre, apellido_paterno, apellido_materno FROM Usuario WHERE ID = {current_user.id}"
        cursor.execute(sql)
        user_details = cursor.fetchone()

    # Combina los campos de nombre, apellido_paterno y apellido_materno para obtener el nombre completo del usuario
    usuario_nombre_completo = f"{user_details['nombre']} {user_details['apellido_paterno']} {user_details['apellido_materno']}"

    
    if form.validate_on_submit():
        if 'save_to_db' in request.form:
            # Lógica para guardar los datos en la base de datos sin redireccionar
            descripcion = form.descripcion.data
            numero = form.numero.data
            cantidad = form.cantidad.data
            unidad = form.unidad.data
            medida = form.medida.data
            fecha_solicitud = datetime.now()
            usuario_solicitante_id = current_user.id

            conn = get_connection()
            with conn.cursor() as cursor:
                sql = "INSERT INTO Solicitud (fecha_solicitud, area_solicitante, descripcion, usuario_solicitante, material, numero_requisicion, unidad_de_medida, cantidad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (fecha_solicitud, current_user.area, descripcion, usuario_solicitante_id, unidad, numero, medida, cantidad))
                conn.commit()

            session['numero_peticion'] = numero
            session['descripcion'] = descripcion
            print(numero)
            print(descripcion)
        else:
            # Lógica para redireccionar a la página de solicitud exitosa
            descripcion = form.descripcion.data
            numero = form.numero.data
            # Resto de la lógica para redireccionar
            return redirect(url_for('auth.solicitud_exitosa', numero_peticion=numero, descripcion=descripcion))

    form.usuario_nombre_completo.data = usuario_nombre_completo
    return render_template('auth/crear_solicitud.html', form=form)
# Definir la vista para mostrar el mensaje de éxito y llamar a la función para generar el PDF y enviar el correo
@auth_blueprint.route('/solicitud_exitosa', methods=['GET', 'POST'])
@login_required
def solicitud_exitosa():
    try:
        # Obtener el número de petición y descripción de los argumentos de la solicitud
        numero_peticion = request.args.get('numero_peticion', '')
        descripcion = request.args.get('descripcion', '')

        form = SolicitudForm()

        # Asignar los valores a los campos del formulario
        form.numero.data = numero_peticion
        form.descripcion.data = descripcion

        # Imprimir el contenido de las variables para verificar si tienen un valor
        print("Número de petición:", numero_peticion)
        print("Descripción:", descripcion)

        # Llamar a la función para generar el PDF y enviar el correo electrónico
        generar_pdf_y_enviar_correo(numero_peticion, descripcion)

        return render_template('auth/solicitud_exitosa.html', numero_peticion=numero_peticion, descripcion=descripcion, form=form)
    except Exception as e:
        error_message = f"Ocurrió un error: {str(e)}"
        return render_template('auth/error.html', error_message=error_message)


@auth_blueprint.route('/Peticiones/buscar', methods=['GET', 'POST'])
@login_required
def Peticionesbuscar():
    # Crear un cursor
    conn = get_connection()
    with conn.cursor() as cursor:
        if request.method == 'POST':
            # Obtener los campos del formulario de búsqueda
            usuario_solicitante = request.form.get('usuario_solicitante')
            numero_solicitud = request.form.get('numero_solicitud')

            # Construir la consulta SQL con los campos de búsqueda
            sql = "SELECT * FROM Solicitud WHERE 1=1"
            params = []

            if usuario_solicitante:
                sql += " AND usuario_solicitante = %s"
                params.append(usuario_solicitante)

            if numero_solicitud:
                sql += " AND numero_requisicion = %s"
                params.append(numero_solicitud)

            sql += " ORDER BY fecha_solicitud DESC"

            # Ejecutar la consulta SQL con los parámetros de búsqueda
            cursor.execute(sql, params)
        else:
            # Si no se envió una solicitud POST, obtener todos los datos de la vista ordenados por fecha descendente
            sql = "SELECT * FROM Solicitud ORDER BY fecha_solicitud DESC"
            cursor.execute(sql)

        # Recuperar los resultados
        peticiones = cursor.fetchall()

        # Cerrar el cursor
        cursor.close()

        # Agrupar las peticiones por usuario y número de petición
        peticiones_agrupadas = {}
        for peticion in peticiones:
            key = (peticion['usuario_solicitante'], peticion['numero_requisicion'])
            if key in peticiones_agrupadas:
                peticiones_agrupadas[key]['detalles'].append(peticion)
            else:
                usuario_nombre_completo = obtener_nombre_completo_usuario(peticion['usuario_solicitante'])
                peticiones_agrupadas[key] = {
                    'usuario_nombre_completo': usuario_nombre_completo,
                    'detalles': [peticion]
                }

        # Convertir el diccionario a una lista de grupos de peticiones
        peticiones_agrupadas = list(peticiones_agrupadas.values())

        # Renderizar la plantilla HTML 'Peticiones.html' con los datos de los usuarios
        return render_template('auth/Peticiones.html', peticiones=peticiones_agrupadas)

def obtener_nombre_completo_usuario(usuario_id):
    
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = f"SELECT nombre, apellido_paterno, apellido_materno FROM Usuario WHERE ID = {usuario_id}"
        cursor.execute(sql)
        user_details = cursor.fetchone()

    usuario_nombre_completo = f"{user_details['nombre']} {user_details['apellido_paterno']} {user_details['apellido_materno']}"
    return usuario_nombre_completo

def obtener_nombre_area(area_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "SELECT nombre FROM Area WHERE ID = %s"
        cursor.execute(sql, (area_id,))
        area_details = cursor.fetchone()

    if area_details:
        nombre_area = area_details['nombre']
        print(nombre_area)
        return nombre_area
    else:
        return "Área Desconocida"  # Manejar el caso si no se encuentra el área


@auth_blueprint.route('/Peticiones', methods=['GET', 'POST'])
@login_required
def Peticiones():
    # Crear un cursor
    conn = get_connection()
    with conn.cursor() as cursor:
        # Ejecutar una consulta para seleccionar todos los datos de la vista, ordenados por fecha descendente
        sql = "SELECT * FROM Solicitud ORDER BY fecha_solicitud DESC"
        cursor.execute(sql)

        # Recuperar los resultados
        peticiones = cursor.fetchall()
        print(peticiones)  # Verificar los datos recuperados

        # Cerrar el cursor
        cursor.close()

        # Agrupar las peticiones por usuario y número de petición
        peticiones_agrupadas = {}
       # Dentro de la función Peticiones()
        for peticion in peticiones:
            key = (peticion['usuario_solicitante'], peticion['numero_requisicion'])
            if key in peticiones_agrupadas:
                peticiones_agrupadas[key]['detalles'].append(peticion)
            else:
                usuario_nombre_completo = obtener_nombre_completo_usuario(peticion['usuario_solicitante'])
                nombre_area = obtener_nombre_area(peticion['area_solicitante'])
                peticiones_agrupadas[key] = {
                    'usuario_nombre_completo': usuario_nombre_completo,
                    'nombre_area': nombre_area,
                    'detalles': [peticion]
                }


        # Convertir el diccionario a una lista de grupos de peticiones
        peticiones_agrupadas = list(peticiones_agrupadas.values())
        #print('peticion:',peticiones_agrupadas)  # Verificar los datos agrupados
        print('hola')  # Verificar si la función se está ejecutando

        # Renderizar la plantilla HTML 'Peticiones.html' con los datos de los usuarios
        return render_template('auth/Peticiones.html', peticiones=peticiones_agrupadas, obtener_nombre_area=obtener_nombre_area)

@auth_blueprint.route('/Peticiones_echas', methods=['GET', 'POST'])
@login_required
def Peticionesuser():
    # Crear un cursor
    conn = get_connection()
    with conn.cursor() as cursor:
        # Ejecutar una consulta para seleccionar todos los datos de la vista, ordenados por fecha descendente
        sql = f"SELECT * FROM Solicitud WHERE usuario_solicitante = {current_user.id}"
        cursor.execute(sql)
        # Resto del código...

        # Recuperar los resultados
        peticiones = cursor.fetchall()
        print(peticiones)  # Verificar los datos recuperados

        # Cerrar el cursor
        cursor.close()

        # Agrupar las peticiones por usuario y número de petición
        peticiones_agrupadas = {}
       # Dentro de la función Peticiones()
        for peticion in peticiones:
            key = (peticion['usuario_solicitante'], peticion['numero_requisicion'])
            if key in peticiones_agrupadas:
                peticiones_agrupadas[key]['detalles'].append(peticion)
            else:
                usuario_nombre_completo = obtener_nombre_completo_usuario(peticion['usuario_solicitante'])
                nombre_area = obtener_nombre_area(peticion['area_solicitante'])
                peticiones_agrupadas[key] = {
                    'usuario_nombre_completo': usuario_nombre_completo,
                    'nombre_area': nombre_area,
                    'detalles': [peticion]
                }


        # Convertir el diccionario a una lista de grupos de peticiones
        peticiones_agrupadas = list(peticiones_agrupadas.values())
        #print('peticion:',peticiones_agrupadas)  # Verificar los datos agrupados
        print('hola')  # Verificar si la función se está ejecutando

        # Renderizar la plantilla HTML 'Peticiones.html' con los datos de los usuarios
        return render_template('auth/Peticionesuser.html', peticiones=peticiones_agrupadas, obtener_nombre_area=obtener_nombre_area)


@auth_blueprint.route('/aprobar_solicitud/<int:ID>')

@login_required
def aprobar_solicitud(ID):
    # Obtener el ID de la solicitud seleccionada desde la URL
    solicitud_id = ID

    # Obtener el ID del usuario que inició sesión
    responsable_aprobacion = current_user.id

    # Obtener la fecha actual
    fecha_actual = date.today()

    # Obtener una conexión a la base de datos
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            # Verificar si el ID de la solicitud ya existe en la tabla "Aprobacion"
            select_sql = "SELECT solicitud_id FROM Aprobacion WHERE solicitud_id = %s"
            cursor.execute(select_sql, (solicitud_id,))
            result = cursor.fetchone()

            if result:
                # Si el ID ya existe, redirigir a una página de aviso
                return render_template('auth/aviso.html', mensaje='El ID de la solicitud ya ha sido aprobado.')

            else:
                # Insertar los datos en la tabla "Aprobacion"
                insert_sql = "INSERT INTO Aprobacion (solicitud_id, fecha_aprobacion, responsable_aprobacion) VALUES (%s, %s, %s)"
                values = (solicitud_id, fecha_actual, responsable_aprobacion)
                cursor.execute(insert_sql, values)

                # Confirmar los cambios en la base de datos
                conn.commit()

    finally:
        # Cerrar la conexión a la base de datos
        conn.close()

    # Redirigir a la página de peticiones después de aprobar la solicitud
    return redirect(url_for('auth.Peticiones'))


@auth_blueprint.route('/Aseptadas')
@login_required
def Aseptadas():
    # Crear una conexión a la base de datos
    conn = get_connection()

    try:
        # Crear un cursor
        with conn.cursor() as cursor:
            # Ejecutar la consulta
            sql = """
             SELECT * FROM VistaSolicitudAprobacion
            """
            cursor.execute(sql)

            # Obtener los resultados de la consulta
            usuarios = cursor.fetchall()
           
        # Cerrar el cursor
        cursor.close()

        # Renderizar la plantilla HTML con los datos de los usuarios
        return render_template('auth/Aseptadas.html', usuarios=usuarios)

    except Exception as e:
        # Manejar cualquier error que ocurra durante el proceso
        print(f"Error al obtener las peticiones: {e}")

    finally:
        # Cerrar la conexión
        conn.close()


@auth_blueprint.route('/Aseptadas/buscar',  methods=['GET', 'POST'])
@login_required
def buscar_Aseptadas():
    # Crear un cursor
    conn = get_connection()
    with conn.cursor() as cursor:
        if request.method == 'POST':
            # Obtener el criterio de búsqueda del formulario
            search_term = request.form.get('search_term')

            # Construir la consulta SQL con el criterio de búsqueda
            sql = "SELECT * FROM VistaSolicitudAprobacion WHERE area_solicitante LIKE %s OR usuario_solicitante LIKE %s ORDER BY fecha_solicitud DESC"

            
            
            # Ejecutar la consulta SQL con el parámetro de búsqueda
            cursor.execute(sql, (f"%{search_term}%", f"%{search_term}%"))

            # Recuperar los resultados
            usuarios = cursor.fetchall()

            # Cerrar el cursor
            cursor.close()

            # Renderizar la plantilla HTML con los datos de los usuarios
            return render_template('auth/Aseptadas.html', usuarios=usuarios)

        else:
            # Si no se envió una solicitud POST, redirigir a la página 'vista_de_area' con GET
            return redirect(url_for('auth.Aseptadas'))

import datetime


@auth_blueprint.route('/surtir_aceptacion/<int:solicitud_id>', methods=['GET', 'POST'])
@login_required
def surtir_aceptacion(solicitud_id):
    # Resto del código...

    # Obtener la solicitud por su ID
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM Solicitud WHERE ID = %s"
        cursor.execute(sql, (solicitud_id,))
        solicitud = cursor.fetchone()

    if solicitud is None:
        flash('La solicitud no existe', 'error')
        return redirect(url_for('auth.Aseptadas'))

    # Verificar si la solicitud ya ha sido surtida
    with conn.cursor() as cursor:
        sql = "SELECT * FROM Surtidas WHERE solicitud_id = %s"
        cursor.execute(sql, (solicitud_id,))
        surtida = cursor.fetchone()

    if surtida is not None:
        flash('La solicitud ya ha sido surtida', 'error')
        return redirect(url_for('auth.Aseptadas'))

    # Obtener el nombre del material requerido por la solicitud
    nombre_material = solicitud['material']

    # Obtener el material por su nombre
    with conn.cursor() as cursor:
        sql = "SELECT * FROM Material WHERE nombre = %s"
        cursor.execute(sql, (nombre_material,))
        material = cursor.fetchone()

    # Resto del código...

    # Resto del código...

    # Resto del código...

    if request.method == 'POST':
        cantidad = cantidad_material

        if cantidad is None or not isinstance(cantidad, int):
            flash('La cantidad ingresada es inválida', 'error')
            print('La cantidad ingresada es inválida', 'error')
            return redirect(url_for('auth.surtir_aceptacion', solicitud_id=solicitud_id))

        cantidad = int(cantidad)

        # Verificar si hay suficiente material disponible
        if cantidad > material['cantidad_disponible']:
            print('No hay suficiente material disponible', 'error')
            flash('No hay suficiente material disponible', 'error')
            return redirect(url_for('auth.Aseptadas'))

        # Realizar la operación de surtido
        fecha_surtido = datetime.date.today()
        responsable = current_user.id

        with conn.cursor() as cursor:
            sql = "INSERT INTO Surtidas (solicitud_id, fecha_surtido, responsable) VALUES (%s, %s, %s)"
            cursor.execute(sql, (solicitud_id, fecha_surtido, responsable))
            conn.commit()

            # Actualizar la cantidad de material en la tabla Material
            nueva_cantidad_material = material['cantidad_disponible'] - cantidad
            sql = "UPDATE Material SET cantidad = %s WHERE ID = %s"
            cursor.execute(sql, (nueva_cantidad_material, material['ID']))
            conn.commit()

        flash('La solicitud ha sido surtida exitosamente', 'success')
        return redirect(url_for('auth.Aseptadas'))

    return render_template('auth/surtir_aceptacion.html', solicitud=solicitud, material=material)



import os
import pandas as pd
from openpyxl import load_workbook
from fpdf import FPDF
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, send_file

from flask import Flask, render_template, send_file
from xhtml2pdf import pisa

# ...

# Función para generar el informe en PDF





@auth_blueprint.route('/llenar_tabla', methods=['GET', 'POST'])
@login_required

def llenar_tabla():
    form = LlenarTablaForm()
    if form.validate_on_submit():
        # Obtener los datos ingresados en el formulario
        nombre = form.nombre.data
        direccion = form.direccion.data
        ciudad = form.ciudad.data
        telefono = form.telefono.data
        correo_electronico = form.correo_electronico.data
        
        conn = get_connection()
        with conn.cursor() as cursor:
            sql = "INSERT INTO Proveedores (nombre, direccion, ciudad, telefono, correo_electronico) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (nombre, direccion, ciudad, telefono, correo_electronico))
            conn.commit()

        # Redireccionar a la página deseada después de guardar los datos
        return redirect(url_for('auth.llenar_tabla'))

    return render_template('auth/llenar_tabla.html', form=form)





@auth_blueprint.route('/mostrar_Provedores', methods=['GET'])
@login_required
def mostrar_Provedores():
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM Proveedores"
        cursor.execute(sql)
        proveedores = cursor.fetchall()

    return render_template('auth/mostrar_Provedores.html', proveedores=proveedores)

@auth_blueprint.route('/mostrar_Provedores', methods=['GET', 'POST'])
@login_required
def mostrar_Provedoresbuscar():
    conn = get_connection()
    with conn.cursor() as cursor:
        if request.method == 'POST':
            # Obtener el criterio de búsqueda del formulario
            search_term = request.form.get('search_term')

            # Construir la consulta SQL con el criterio de búsqueda
            sql = "SELECT * FROM Proveedores WHERE nombre LIKE %s OR ciudad LIKE %s"
            
            # Ejecutar la consulta SQL con el parámetro de búsqueda
            cursor.execute(sql, (f"%{search_term}%", f"%{search_term}%"))
        else:
            sql = "SELECT * FROM Proveedores"
            cursor.execute(sql)

        proveedores = cursor.fetchall()

    return render_template('auth/mostrar_Provedores.html', proveedores=proveedores)

@auth_blueprint.route('/llenar_tabla/editar/<int:proveedor_id>', methods=['GET', 'POST'])
@login_required
def editar_proveedor(proveedor_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        # Obtener los datos del proveedor a editar
        sql = "SELECT * FROM Proveedores WHERE ID = %s"
        cursor.execute(sql, (proveedor_id,))
        proveedor = cursor.fetchone()

    form = LlenarTablaeditarForm()
    if request.method == 'POST' and form.validate_on_submit():
        nombre = form.nombre.data
        direccion = form.direccion.data
        ciudad = form.ciudad.data
        telefono = form.telefono.data
        correo_electronico = form.correo_electronico.data

        conn = get_connection()
        with conn.cursor() as cursor:
            sql = "UPDATE Proveedores SET nombre = %s, direccion = %s, ciudad = %s, telefono = %s, correo_electronico = %s WHERE ID = %s"
            cursor.execute(sql, (nombre, direccion, ciudad, telefono, correo_electronico, proveedor_id))
            conn.commit()

        return redirect(url_for('auth.llenar_tabla'))

    # Rellenar el formulario con los datos del proveedor a editar
    form.nombre.data = proveedor['nombre']
    form.direccion.data = proveedor['direccion']
    form.ciudad.data = proveedor['ciudad']
    form.telefono.data = proveedor['telefono']
    form.correo_electronico.data = proveedor['correo_electronico']

    return render_template('auth/editar_proveedor.html', form=form, proveedor=proveedor)


@auth_blueprint.route('/llenar_tabla/borrar/<int:proveedor_id>', methods=['GET', 'POST'])
@login_required
def borrar_proveedor(proveedor_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        # Obtener los datos del proveedor a borrar
        sql = "SELECT * FROM Proveedores WHERE ID = %s"
        cursor.execute(sql, (proveedor_id,))
        proveedor = cursor.fetchone()

        # Eliminar el proveedor de la base de datos
        sql = "DELETE FROM Proveedores WHERE ID = %s"
        cursor.execute(sql, (proveedor_id,))
        conn.commit()

    return redirect(url_for('auth.llenar_tabla'))




import time
from flask import redirect, url_for, flash
from datetime import datetime, timedelta
from flask_login import logout_user, current_user







@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import base64
import os
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import base64
import os
import io
import base64
from flask import after_this_request

@auth_blueprint.route('/grafica')
@login_required
def grafica():
    # Crear un cursor
    conn = get_connection()
    with conn.cursor() as cursor:
        # Ejecutar una consulta para seleccionar todos los datos de la vista
        sql = "SELECT * FROM Material"
        cursor.execute(sql)

        # Recuperar los resultados
        usuarios = cursor.fetchall()
        print(usuarios)

        # Cerrar el cursor
        cursor.close()

        # Crear una lista de nombres de productos y cantidades
        nombres = [usuario['nombre'] for usuario in usuarios]

        cantidades = [usuario['cantidad_disponible'] for usuario in usuarios]

        # Obtener la ruta del directorio actual
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Crear una ruta para el directorio temporal
        temp_dir = os.path.join(current_dir, 'temp')

        # Crear el directorio si no existe
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Crear la ruta completa para el archivo de la gráfica
        chart_path = os.path.join(temp_dir, 'chart.png')

        # Generar la gráfica de pastel
        plt.pie(cantidades, labels=nombres, autopct='%1.1f%%')

        # Guardar la gráfica en un objeto BytesIO
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Leer el contenido del objeto BytesIO en base64
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        @after_this_request
        def add_header(response):
            plt.close()  # Cerrar la figura para liberar memoria
            return response

        # Renderizar la plantilla HTML con los datos y la gráfica
        return render_template('admin/User.html', usuarios=usuarios, image_base64=image_base64)
######################################################################











# Definir la vista para mostrar el mensaje de éxito y llamar a la función para generar el PDF y enviar el correo



def get_materiales():
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "SELECT ID, nombre FROM Material"
        cursor.execute(sql)
        materiales = cursor.fetchall()
    return materiales


@auth_blueprint.route('/aceptacion', methods=['GET', 'POST'])
@login_required
def aceptacion():
    form = AceptadasForm()
    form.material.choices = [(material['ID'], material['nombre']) for material in get_materiales()]
    conn = get_connection()
    with conn.cursor() as cursor:
        if form.validate_on_submit():

            if 'save_to_db' in request.form:
                descripcion_formulario = form.descripcion.data
                numero_requisicion = form.numero_requisicion.data
                cantidad = form.cantidad.data
                medida = form.unidad_de_medida.data
                 
                fecha_solicitud = datetime.now()
                usuario_solicitante = form.usuario_solicitante.data
                area_solicitante = form.area_solicitante.data
                numero_peticion_formulario = form.numero_peticion.data
                concepto = form.concepto.data
                responsable_aprobacion = form.responsable_aprobacion.data
                material_id = form.material.data  # Obtén el ID del material seleccionado

                # Verificar si hay suficiente cantidad de material
                sql_check_quantity = "SELECT cantidad_disponible FROM Material WHERE ID = %s"
                cursor.execute(sql_check_quantity, (material_id,))
                material_row = cursor.fetchone()
                #print('comprueva:',material_row)
                if material_row and material_row['cantidad_disponible'] >= cantidad:
                    # Restar la cantidad de material seleccionado
                    sql_update_quantity = "UPDATE Material SET cantidad_disponible = cantidad_disponible - %s WHERE ID = %s"
                    cursor.execute(sql_update_quantity, (cantidad, material_id))

                    # Insertar la solicitud en la base de datos
                    sql_insert_solicitud = "INSERT INTO aceptadas (fecha_solicitud, area_solicitante, descripcion, usuario_solicitante, material, numero_requisicion, unidad_de_medida, cantidad, numero_peticion, concepto, responsable_aprobacion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql_insert_solicitud, (fecha_solicitud, area_solicitante, descripcion_formulario, usuario_solicitante, material_id, numero_requisicion, medida, cantidad, numero_peticion_formulario, concepto, responsable_aprobacion))
                    conn.commit()

                    #print(session['numero_peticion'])

                    session['numero_peticion'] = numero_peticion_formulario
                    session['descripcion'] = descripcion_formulario

                    #print('numero:',numero_peticion_formulario)
                    #print(descripcion_formulario)
                else:
                    # Redirigir a la página de cantidad insuficiente
                    return redirect(url_for('auth.cantidad_insuficiente'))

            else:
                descripcion_formulario = form.descripcion.data
                numero_peticion_formulario = form.numero_peticion.data
                
                
                return redirect(url_for('auth.aceptacion_exitosa', numero_peticion=numero_peticion_formulario, descripcion=descripcion_formulario))


        # Obtener los campos del formulario de búsqueda
        usuario_solicitante = request.form.get('usuario_solicitante')
        numero_solicitud = request.form.get('numero_solicitud')

        # Construir la consulta SQL con los campos de búsqueda
        sql = "SELECT * FROM Solicitud WHERE 1=1"
        params = []

        if usuario_solicitante:
            sql += " AND usuario_solicitante = %s"
            params.append(usuario_solicitante)

        if numero_solicitud:
            sql += " AND numero_requisicion = %s"
            params.append(numero_solicitud)

        sql += " ORDER BY fecha_solicitud DESC"

        # Ejecutar la consulta SQL con los parámetros de búsqueda
        cursor.execute(sql, params)

        # Recuperar los resultados
        peticiones = cursor.fetchall()

        # Agrupar las peticiones por usuario y número de petición
        peticiones_agrupadas = {}
        for peticion in peticiones:
            key = (peticion['usuario_solicitante'], peticion['numero_requisicion'])
            if key in peticiones_agrupadas:
                peticiones_agrupadas[key]['detalles'].append(peticion)
            else:
                usuario_nombre_completo = obtener_nombre_completo_usuario(peticion['usuario_solicitante'])
                peticiones_agrupadas[key] = {
                    'usuario_nombre_completo': usuario_nombre_completo,
                    'detalles': [peticion]
                }

        # Convertir el diccionario a una lista de grupos de peticiones
        peticiones_agrupadas = list(peticiones_agrupadas.values())

        if request.method == 'POST':
                
            try:
                # Obtener el criterio de búsqueda del formulario
                search_term = request.form.get('search_term')

                # Construir la consulta SQL con el criterio de búsqueda para los materiales
                sql_material = "SELECT * FROM Material WHERE nombre LIKE %s OR descripcion LIKE %s"

                # Ejecutar la consulta SQL con el parámetro de búsqueda
                cursor.execute(sql_material, (f"%{search_term}%", f"%{search_term}%"))

                # Recuperar los resultados
                materiales = cursor.fetchall()

                # Crear una lista para almacenar los detalles de los materiales, incluido el nombre del proveedor
                materiales_con_detalles = []

                # Recorrer cada material y obtener el nombre del proveedor correspondiente
                for material in materiales:
                    proveedor_id = material['proveedor_id']

                    # Obtener el nombre del proveedor usando el proveedor_id
                    sql_prov = "SELECT nombre FROM Proveedores WHERE ID = %s"
                    cursor.execute(sql_prov, (proveedor_id,))
                    proveedor = cursor.fetchone()

                    # Crear un nuevo diccionario con los detalles del material, incluido el nombre del proveedor
                    material_con_detalles = {
                        'ID': material['ID'],
                        'nombre': material['nombre'],
                        'descripcion': material['descripcion'],
                        'cantidad': material['cantidad_disponible'],
                        'lote': material['lote'],
                        'fecha': material['fecha_registro'],
                        'proveedor': proveedor['nombre'] if proveedor else 'Proveedor no encontrado'
                    }

                    # Agregar el diccionario a la lista de materiales con detalles
                    materiales_con_detalles.append(material_con_detalles)
            except Exception as e:
                # Manejar errores de consulta
                print("Error en la consulta de materiales:", e)
                materiales_con_detalles = []
        else:
            # Si no se envió una solicitud POST, obtener todos los datos de la tabla Material
            sql_material = "SELECT * FROM Material"
            cursor.execute(sql_material)

            # Recuperar los resultados
            materiales = cursor.fetchall()
            materiales_con_detalles = []  # Definir la lista vacía aquí

        return render_template('auth/aceptacion.html', form=form, peticiones=peticiones_agrupadas, materiales=materiales_con_detalles)



def generar_pdf(numero_peticion, descripcion):
    print("Generando PDF para número de petición:", numero_peticion)
    # Resto del código para obtener los datos de la base de datos y generar el DataFrame df
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "SELECT numero_requisicion, descripcion, usuario_solicitante, area_solicitante, fecha_solicitud, material, unidad_de_medida, cantidad, numero_peticion, concepto, responsable_aprobacion FROM aceptadas WHERE numero_requisicion = %s AND descripcion = %s"
        cursor.execute(sql, (numero_peticion, descripcion))
        solicitud_data = cursor.fetchall()
        print(solicitud_data)

    if len(solicitud_data) == 0:
        return "No se encontraron datos para generar el PDF y enviar el correo."

    # Obtener los datos adicionales de la consulta y almacenarlos en variables
    usuario_solicitante = []
    area_solicitante = []
    fecha = []
    material = []
    unidad_de_medida = []
    cantidad = []
    numero_peticion = []
    concepto = []
    responsable_aprobacion = []

    for solicitud in solicitud_data:
        usuario_solicitante.append(solicitud['usuario_solicitante'])
        fecha.append(solicitud['fecha_solicitud'])
        material.append(solicitud['material'])
        unidad_de_medida.append(solicitud['unidad_de_medida'])
        cantidad.append(solicitud['cantidad'])
        numero_peticion.append(solicitud['numero_peticion'])
        concepto.append(solicitud['concepto'])
        responsable_aprobacion.append(solicitud['responsable_aprobacion'])

    # Consultar en BD por usuario_solicitante para obtener los nombres completos de los usuarios
    # Aquí debes agregar el código para obtener los nombres completos y almacenarlos en la variable usuarios_nombres_completos

    # Generar el DataFrame
    # Asegurar que todas las listas tengan la misma longitud
    num_rows = len(solicitud_data)
    area_solicitante = solicitud_data[0]['area_solicitante']
    fecha = [peticion['fecha_solicitud'] for peticion in solicitud_data]
    material = [peticion['material'] for peticion in solicitud_data]
    unidad_de_medida = [peticion['unidad_de_medida'] for peticion in solicitud_data]
    cantidad = [peticion['cantidad'] for peticion in solicitud_data]
    numero_peticion = [peticion['numero_peticion'] for peticion in solicitud_data]
    concepto = [peticion['concepto'] for peticion in solicitud_data]
    responsable_aprobacion = [peticion['responsable_aprobacion'] for peticion in solicitud_data]

    # Crear el DataFrame con las listas actualizadas
    data = {
        'Número de Petición': numero_peticion,
        'Descripción': [descripcion] * num_rows,
        'Nombre del Solicitante': usuario_solicitante,  # Aquí debes usar la variable usuarios_nombres_completos
        'Área Solicitante': [area_solicitante] * num_rows,
        'Fecha': fecha,
        'Material': material,
        'Unidad': unidad_de_medida,
        'Cantidad': cantidad,
        'Concepto': concepto,
        'Responsable de Aprobación': responsable_aprobacion
        # Agrega aquí los demás campos que desees mostrar en el PDF
    }
    df = pd.DataFrame(data)

    # Resto del código para generar el PDF y enviar el correo...

    print('data:', df)  # Puedes imprimir el DataFrame para verificar su contenido



    # Renderizar el archivo HTML utilizando Jinja y almacenar el resultado en una variable
    html = render_template('informe_template.html',  data=df)

    # Agregar declaración de codificación UTF-8 al inicio del archivo HTML
    html = f"<!DOCTYPE html><html><head><meta charset='UTF-8'></head><body>{html}</body></html>"

    # Generar el PDF utilizando pdfkit
    pdf_bytes = pdfkit.from_string(html, False)

    # Enviar el PDF por correo electrónico
    response = make_response(pdf_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={"informe.pdf"}'
    return response


@auth_blueprint.route('/aceptacion_exitosa', methods=['GET', 'POST'])
@login_required
def aceptacion_exitosa():
    # Obtener el número de petición y descripción de los argumentos de la solicitud
    numero_peticion = request.args.get('numero_peticion', '')
    descripcion = request.args.get('descripcion', '')

    form = AceptadasForm()

    # Asignar los valores a los campos del formulario
    form.numero_peticion.data =  numero_peticion 
    form.descripcion.data = descripcion

    # Imprimir el contenido de las variables para verificar si tienen un valor
    #print("Número de petición:", numero_peticion)
    #print("Descripción:", descripcion)

    # Llamar a la función para generar el PDF y enviar el correo electrónico
   
    #print("Generando PDF para número de petición:", numero_peticion)
    # Resto del código para obtener los datos de la base de datos y generar el DataFrame df
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "SELECT numero_requisicion, descripcion, usuario_solicitante, area_solicitante, fecha_solicitud, material, unidad_de_medida, cantidad, numero_peticion, concepto, responsable_aprobacion FROM aceptadas WHERE numero_requisicion = %s AND descripcion = %s"
        cursor.execute(sql, (numero_peticion, descripcion))
        solicitud_data = cursor.fetchall()
        #print(solicitud_data)

    if len(solicitud_data) == 0:
        return redirect(url_for('auth.error_de_red'))

    # Obtener los datos adicionales de la consulta y almacenarlos en variables
    usuario_solicitante = []
    area_solicitante = []
    fecha = []
    material = []
    unidad_de_medida = []
    cantidad = []
    numero_peticion = []
    concepto = []
    responsable_aprobacion = []

    for solicitud in solicitud_data:
        usuario_solicitante.append(solicitud['usuario_solicitante'])
        fecha.append(solicitud['fecha_solicitud'])
        material.append(solicitud['material'])
        unidad_de_medida.append(solicitud['unidad_de_medida'])
        cantidad.append(solicitud['cantidad'])
        numero_peticion.append(solicitud['numero_peticion'])
        concepto.append(solicitud['concepto'])
        responsable_aprobacion.append(solicitud['responsable_aprobacion'])


    materiales_ids = list(set(material))
    materiales_nombres = {}
    with conn.cursor() as cursor:
        for material_id in materiales_ids:
            sql = f"SELECT nombre FROM Material WHERE ID = {material_id}"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                materiales_nombres[material_id] = result['nombre']

    # Reemplazar los IDs de materiales en la lista material con los nombres correspondientes
    material = [materiales_nombres[material_id] if material_id in materiales_nombres else material_id for material_id in material]

    # Generar el DataFrame
    # Asegurar que todas las listas tengan la misma longitud
    num_rows = len(solicitud_data)
    area_solicitante = solicitud_data[0]['area_solicitante']
    fecha = [peticion['fecha_solicitud'] for peticion in solicitud_data]
    material = result['nombre']
    unidad_de_medida = [peticion['unidad_de_medida'] for peticion in solicitud_data]
    cantidad = [peticion['cantidad'] for peticion in solicitud_data]
    numero_peticion = [peticion['numero_peticion'] for peticion in solicitud_data]
    concepto = [peticion['concepto'] for peticion in solicitud_data]
    responsable_aprobacion = [peticion['responsable_aprobacion'] for peticion in solicitud_data]
    numero_coincidencias = len(solicitud_data)


    # Crear el DataFrame con las listas actualizadas
    data = {
        'Número de Petición': numero_peticion,
        'Número': [numero_coincidencias] * num_rows,
        'Descripción': [descripcion] * num_rows,
        'Nombre del Solicitante': usuario_solicitante,  # Aquí debes usar la variable usuarios_nombres_completos
        'Área Solicitante': [area_solicitante] * num_rows,
        'Fecha': fecha,
        'Material': material,
        'Unidad': unidad_de_medida,
        'Cantidad': cantidad,
        'Concepto': concepto,
        'Responsable de Aprobación': responsable_aprobacion
        # Agrega aquí los demás campos que desees mostrar en el PDF
    }
    df = pd.DataFrame(data)

    # Resto del código para generar el PDF y enviar el correo...

    #print('data:', df)  # Puedes imprimir el DataFrame para verificar su contenido



    # Renderizar el archivo HTML utilizando Jinja y almacenar el resultado en una variable
    html = render_template('informe_template1.html',  data=df)

    # Agregar declaración de codificación UTF-8 al inicio del archivo HTML
    html = f"<!DOCTYPE html><html><head><meta charset='UTF-8'></head><body>{html}</body></html>"

    # Generar el PDF utilizando pdfkit
    pdf_bytes = pdfkit.from_string(html, False)

    # Enviar el PDF por correo electrónico
    response = make_response(pdf_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={"informe.pdf"}'
    return response


@auth_blueprint.route('/aceptacion_exitosa_exitosa', methods=['GET', 'POST'])
@login_required
def aceptacion_exitosa_exitosa():
    # Obtener el número de petición y descripción de los argumentos de la solicitud
    numero_peticion = request.args.get('numero_peticion', '')
    descripcion = request.args.get('descripcion', '')

    form = AceptadasForm()

    # Asignar los valores a los campos del formulario
    form.numero_peticion.data =  numero_peticion 
    form.descripcion.data = descripcion

    # Imprimir el contenido de las variables para verificar si tienen un valor
    #print("Número de petición:", numero_peticion)
    #print("Descripción:", descripcion)

    # Llamar a la función para generar el PDF y enviar el correo electrónico
   
    
    

    return render_template('auth/aceptacion_exitosa.html', numero_peticion=numero_peticion, descripcion=descripcion, form=form)


@auth_blueprint.route('/cantidad_insuficiente', methods=['GET', 'POST'])
@login_required
def cantidad_insuficiente():

    return render_template('auth/cantidad_insuficiente.html')



@auth_blueprint.route('/error_de_red', methods=['GET', 'POST'])
@login_required
def error_de_red():

    return render_template('auth/error_de_red.html')
    


@auth_blueprint.route('/solicitudes')
@login_required
def solicitudes():
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = """
        SELECT a.ID, a.fecha_solicitud, a.area_solicitante, a.descripcion, a.usuario_solicitante,
            m.nombre AS material_nombre, a.numero_requisicion, a.unidad_de_medida, a.cantidad,
            a.numero_peticion, a.concepto, a.responsable_aprobacion
        FROM aceptadas a
        INNER JOIN Material m ON a.material = m.ID;

        """
        cursor.execute(sql)
        solicitudes = cursor.fetchall()

    return render_template('auth/solicitudes.html', solicitudes=solicitudes)
