from flask import Blueprint, render_template

home_blueprint = Blueprint('home', __name__)

from .forms import LoginForm, RegisterForm,UpdateForm

from .models import  get_user_by_username, get_user_by_username_and_password
from werkzeug.security import generate_password_hash

from flask_login import login_user, login_required, logout_user
from flask_login import current_user

from db.db_connection import get_connection

from flask_sqlalchemy import SQLAlchemy
from flask import (redirect, render_template, request, 
                Blueprint, url_for)

from .forms import get_user_by_email
from .views import get_connection

from flask import current_app, flash, request
import requests


# Resto del código del archivo forms.py


######## Rutas publicas
@home_blueprint.route('/', methods=['GET', 'POST'])
def index():

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = get_user_by_username_and_password(username, password)

        if user:
            login_user(user)

            if user.tipo == 'Direccion':
                next = request.args.get('next')
                return redirect(next or url_for('home.User', _external=True, _scheme='http'))
            elif user.tipo == 'Area':
                next = request.args.get('next')
                return redirect(next or url_for('home.Area', _external=True, _scheme='http'))
            elif user.tipo == 'Administrador':
                next = request.args.get('next')
                return redirect(next or url_for('home.Admin', _external=True, _scheme='http'))
        else:
            flash("Acceso denegado. Por favor, verifica tus credenciales.", "danger")

    return render_template('auth/login.html', form=form)





from reportlab.pdfgen import canvas

from flask import send_file
from io import BytesIO
from reportlab.pdfgen import canvas

from flask_mail import Message
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# ...

def get_user_by_email(email):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM Usuario WHERE email = %s"
        cursor.execute(sql, (email,))
        user = cursor.fetchone()
    return user
@home_blueprint.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "SELECT ID, nombre FROM Area"
        cursor.execute(sql)
        areas = cursor.fetchall()
    form.area.choices = [(g['ID'], g['nombre']) for g in areas]

    if form.validate_on_submit():
        username = form.username.data
        nombre = form.nombre.data
        apellido_materno = form.apellido_materno.data
        apellido_paterno = form.apellido_paterno.data
        password = form.password.data
        email = form.email.data
        gender = form.gender.data
        area = form.area.data
        
        # Cifrado de contraseña
        hashed_password = generate_password_hash(password)

        conn = get_connection()
        with conn.cursor() as cursor:
            sql = "INSERT INTO Usuario (nombre, apellido_materno, apellido_paterno, contrasena, tipo, username, email, area) "
            sql += f"VALUES ('{nombre}', '{apellido_materno}', '{apellido_paterno}', '{hashed_password}', '{gender}', '{username}', '{email}','{area}')"
            cursor.execute(sql)
            conn.commit()

        # Generar el PDF con los datos del usuario
        pdf_buffer = generate_user_data_pdf(username, nombre, apellido_materno, apellido_paterno, password)

        # Enviar el correo electrónico con el PDF adjunto
        send_email_with_attachment(email, 'Datos de usuario', 'Adjuntamos los datos del usuario en formato PDF.', pdf_buffer, 'user_data.pdf')

        return redirect(url_for('home.Admin'))

    return render_template('auth/register.html', form=form)


def generate_user_data_pdf(username, nombre, apellido_materno, apellido_paterno, password):
    # Generar el PDF con los datos del usuario utilizando una librería como ReportLab o PyPDF2
    # Aquí tienes un ejemplo básico utilizando ReportLab
    from reportlab.pdfgen import canvas

    buffer = BytesIO()

    p = canvas.Canvas(buffer)
    p.drawString(100, 100, f'Username: {username}')
    p.drawString(100, 120, f'Nombre: {nombre}')
    p.drawString(100, 140, f'Apellido Paterno: {apellido_paterno}')
    p.drawString(100, 160, f'Apellido Materno: {apellido_materno}')
    p.drawString(100, 180, f'Contraseña: {password}')
    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer

#iJh_geQgN4ss!Xr
def send_email_with_attachment(to_email, subject, body, attachment_data, attachment_filename):
    # Configurar los detalles de conexión del servidor SMTP
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = '@gmail.com'  # Inserta tu dirección de correo electrónico de Gmail, este correo es el de la organizacion en general,o simplemente se debe crear para esta aplicacion
    smtp_password = 'msfechovcuaflztf'  # Inserta tu contraseña de correo electrónico válida , debe ser clave de aplicasion como lo indica em el manual 

    # Crear el objeto del mensaje
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to_email
    msg['Subject'] = subject

    # Agregar el cuerpo del mensaje
    msg.attach(MIMEText(body, 'plain'))

    # Agregar el archivo adjunto
    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(attachment_data.getvalue())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename={attachment_filename}')
    msg.attach(attachment)

    # Conectar y enviar el correo electrónico
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_email, msg.as_string())


@home_blueprint.route('/register/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "DELETE FROM Usuario WHERE ID = %s"
        cursor.execute(sql, (user_id,))
        conn.commit()
    return redirect(url_for('auth.usuarios'))

@home_blueprint.route('/register/update/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    print("Entro a la función update_user")
    conn = get_connection()
    with conn.cursor() as cursor:
        # Obtener los datos del usuario a actualizar
        sql = "SELECT * FROM Usuario WHERE ID = %s"
        cursor.execute(sql, (user_id,))
        user = cursor.fetchone()

    form = UpdateForm()
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "SELECT ID, nombre FROM Area"
        cursor.execute(sql)
        areas = cursor.fetchall()
    form.area.choices = [(g['ID'], g['nombre']) for g in areas]

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data

        # Verificar si el nuevo nombre de usuario ya está en uso por otro usuario
        if username != user['username']:  # Verifica si el nuevo nombre es diferente del nombre actual
            conn = get_connection()
            with conn.cursor() as cursor:
                sql = "SELECT * FROM Usuario WHERE ID != %s AND username = %s"
                cursor.execute(sql, (user_id, username))
                existing_user = cursor.fetchone()

            if existing_user:
                flash('El nombre de usuario ya está en uso. Por favor, elija otro.')
                return render_template('auth/update_user.html', form=form, user=user)

        # Si el nuevo nombre de usuario está disponible o no se ha cambiado, proceder con la actualización
        nombre = form.nombre.data
        apellido_materno = form.apellido_materno.data
        apellido_paterno = form.apellido_paterno.data
        password = form.password.data
        gender = form.gender.data
        area = form.area.data
       
        # Cifrado de contraseña
        hashed_password = generate_password_hash(password)

        conn = get_connection()
        with conn.cursor() as cursor:
            sql = "UPDATE Usuario SET username = %s, nombre = %s, apellido_materno = %s, apellido_paterno = %s, contrasena = %s, tipo = %s,area = %s WHERE ID = %s"
            cursor.execute(sql, (username, nombre, apellido_materno, apellido_paterno, hashed_password, gender,area,user_id))
            conn.commit()

        flash('Usuario actualizado con éxito.')
        return redirect(url_for('home.Admin'))

    # Rellenar el formulario con los datos del usuario a actualizar
    form.username.data = user['username']
    form.nombre.data = user['nombre']
    form.apellido_materno.data = user['apellido_materno']
    form.apellido_paterno.data = user['apellido_paterno']
    form.gender.data = user['tipo']
    form.area.data = user['area']

    return render_template('auth/update_user.html', form=form, user=user)




@home_blueprint.route('/contact')
def contact():
    return render_template('home/contact.html')

@home_blueprint.route('/manual')
def manual():
    
    return render_template('home/manual.html')

@home_blueprint.route('/Seguridad')
def Seguridad():
    
    return render_template('home/Seguridad.html')


@home_blueprint.route('/Acerca_de')
def Acerca_de():
    
    return render_template('home/Acerca_de.html')





import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import base64
import os
import io
import base64
import pandas as pd

def grafica():
    # Crear un cursor
    conn = get_connection()
    with conn.cursor() as cursor:
        # Ejecutar una consulta para seleccionar todos los datos de la vista
        sql = "SELECT * FROM Material"
        cursor.execute(sql)

        # Recuperar los resultados
        usuarios = cursor.fetchall()

        # Cerrar el cursor
        cursor.close()

        # Crear una lista de nombres de productos y cantidades positivas
        nombres = []
        cantidades_positivas = []

        for usuario in usuarios:
            nombre = usuario['nombre']
            cantidad = usuario['cantidad_disponible']

            if cantidad > 0:
                nombres.append(nombre)
                cantidades_positivas.append(cantidad)

        # Si no hay cantidades mayores a cero, retornar un diccionario ficticio
        if not cantidades_positivas:
            return {'image_base64': 'imagen_no_disponible'}

        # Generar la gráfica de pastel
        plt.pie(cantidades_positivas, labels=nombres, autopct='%1.1f%%')

        # Guardar la gráfica en un objeto BytesIO
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Leer el contenido del objeto BytesIO en base64
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # Cerrar la figura para liberar memoria
        plt.close()

        # Retornar el resultado de la gráfica
        return {'image_base64': image_base64}



@home_blueprint.route("/User")
@login_required
def User():
    user_id = current_user.get_id()

    if user_id is None:
        return redirect(url_for('home.index'))

    # Verifica el tipo de usuario antes de permitir el acceso
    if current_user.tipo != 'Direccion':
        flash("Acceso denegado. No tienes permiso para acceder a esta página.", "danger")
        return redirect(url_for('home.index'))
    # Comprobar si el usuario tiene una sesión iniciada

    # Generar la gráfica llamando a la función grafica()
    grafica_result = grafica()

    # Obtener los resultados de la gráfica
    image_base64 = grafica_result.get('image_base64')

    usuario_correo = "edwin.nol2.123@gmail.com"  # Reemplaza con tu dirección de correo electrónico
    contrasena = "msfechovcuaflztf"  # Reemplaza con tu contraseña
    mensajes = obtener_mensajes_bandeja_entrada(usuario_correo, contrasena)

    # Llamar a la función Peticiones() para obtener los datos de los usuarios
    #usuarios = Peticiones()

    # Renderizar la plantilla HTML con los datos y la gráfica
    return render_template('admin/user.html',  image_base64=image_base64,mensajes=mensajes)


def Peticiones():
    # Crear un cursor
    conn = get_connection()
    with conn.cursor() as cursor:
        # Ejecutar una consulta para seleccionar todos los datos de la vista, ordenados por fecha descendente
        sql = "SELECT * FROM Solicitud ORDER BY fecha_solicitud DESC"
        cursor.execute(sql)

        # Recuperar los resultados
        usuarios = cursor.fetchall()

        # Calcular el porcentaje de progreso para cada usuario (ejemplo: valor fijo del 50%)
        for usuario in usuarios:
            usuario['porcentaje'] = 50

        # Cerrar el cursor
        cursor.close()

        # Renderizar la plantilla HTML 'admin/user.html' con los datos de los usuarios
        

        # Retornar los datos de los usuarios
        return usuarios


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

@home_blueprint.route("/Area")
@login_required
def Area():
    user_id = current_user.get_id()

    if user_id is None:
        return redirect(url_for('home.index'))

    # Verifica el tipo de usuario antes de permitir el acceso
    if current_user.tipo != 'Area':
        flash("Acceso denegado. No tienes permiso para acceder a esta página.", "danger")
        return redirect(url_for('home.index'))



     
    
    # Comprobar si el usuario tiene una sesión iniciada
    
    return render_template('user/area.html')





def vista_de_area():
    # Crear un cursor
    conn = get_connection()
    with conn.cursor() as cursor:
        # Ejecutar una consulta para seleccionar todos los datos de la vista
        sql = "SELECT * FROM Area"
        cursor.execute(sql)

        # Recuperar los resultados
        areas = cursor.fetchall()

        # Cerrar el cursor
        cursor.close()

        # Renderizar la plantilla HTML con los datos de los usuarios
        return areas


@home_blueprint.route("/Admin")
@login_required
def Admin():
    user_id = current_user.get_id()

    if user_id is None:
        return redirect(url_for('home.index'))

    # Verifica el tipo de usuario antes de permitir el acceso
    if current_user.tipo != 'Administrador':
        flash("Acceso denegado. No tienes permiso para acceder a esta página.", "danger")
        return redirect(url_for('home.index'))

    areas = vista_de_area()
    #print(areas)
    resultados_usuarios = usuarios()
    print(resultados_usuarios)

    # Comprobar si el usuario tiene una sesión iniciada

    return render_template('root/admin.html',resultados_usuarios=resultados_usuarios, areas=areas)


def usuarios():
    # Crear un cursor
    conn = get_connection()
    with conn.cursor() as cursor:
        # Ejecutar una consulta para seleccionar todos los datos de la vista
        sql = "SELECT * FROM Usuario"
        cursor.execute(sql)

        # Recuperar los resultados
        resultados_usuarios = cursor.fetchall()

        # Imprimir los resultados para verificar
        print(resultados_usuarios)
        
        # Cerrar el cursor
        cursor.close()

        # Renderizar la plantilla HTML con los datos de los usuarios
        return resultados_usuarios


from datetime import datetime, timedelta

# ...

from flask_login import logout_user

@home_blueprint.route('/dashboard')
@login_required
def dashboard():
    # Resto del código...

    # Actualizar la marca de tiempo de la última actividad del usuario
    current_user.update_last_seen()

    # Verificar si ha pasado un tiempo suficiente desde la última actividad
    inactive_duration = datetime.now() - current_user.last_seen

    # Duración de inactividad permitida (por ejemplo, 30 minutos)
    max_inactive_duration = timedelta(minutes=1)

    if inactive_duration > max_inactive_duration:
        logout_user()
        flash('Tu sesión ha sido cerrada debido a la inactividad', 'info')
        return redirect(url_for('home./'))

    return render_template('home/dashboard.html')



from flask import redirect, url_for
def redirect_based_on_user_type(user):
    if user.tipo == 'Direccion':
        next_page = request.args.get('next')
        return redirect(next_page or url_for('home.User'))
    elif user.tipo == 'Area':
        next_page = request.args.get('next')
        return redirect(next_page or url_for('home.Area'))
    elif user.tipo == 'Administrador':
        next_page = request.args.get('next')
        return redirect(next_page or url_for('home.Admin'))
    else:
        return redirect(url_for('error404'))  # Redirigir a página de error 404

@home_blueprint.route('/redirect')
def redirect_route():
    if current_user.is_authenticated:
        return redirect_based_on_user_type(current_user)
    else:
        return redirect(url_for('home.index'))






########################administracion de perfil de usuario 




@home_blueprint.route('/update/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update(user_id):
    # Verificar si el usuario actual está autorizado para actualizar este usuario
    if current_user.id != user_id:
        flash('No tienes permiso para actualizar este usuario.')
        return redirect(url_for('home.Admin'))  # Redireccionar a donde quieras

    # Resto de tu código para la función de actualización
    conn = get_connection()
    with conn.cursor() as cursor:
        # Obtener los datos del usuario a actualizar
        sql = "SELECT * FROM Usuario WHERE ID = %s"
        cursor.execute(sql, (user_id,))
        user = cursor.fetchone()

    form = UpdateForm()
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "SELECT ID, nombre FROM Area"
        cursor.execute(sql)
        areas = cursor.fetchall()
    form.area.choices = [(g['ID'], g['nombre']) for g in areas]

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data

        # Verificar si el nuevo nombre de usuario ya está en uso por otro usuario
        if username != user['username']:  # Verifica si el nuevo nombre es diferente del nombre actual
            conn = get_connection()
            with conn.cursor() as cursor:
                sql = "SELECT * FROM Usuario WHERE ID != %s AND username = %s"
                cursor.execute(sql, (user_id, username))
                existing_user = cursor.fetchone()

            if existing_user:
                flash('El nombre de usuario ya está en uso. Por favor, elija otro.')
                return render_template('auth/update_user.html', form=form, user=user)

        # Si el nuevo nombre de usuario está disponible o no se ha cambiado, proceder con la actualización
        nombre = form.nombre.data
        apellido_materno = form.apellido_materno.data
        apellido_paterno = form.apellido_paterno.data
        password = form.password.data
        gender = form.gender.data
        area = form.area.data
       
        # Cifrado de contraseña
        hashed_password = generate_password_hash(password)

        conn = get_connection()
        with conn.cursor() as cursor:
            sql = "UPDATE Usuario SET username = %s, nombre = %s, apellido_materno = %s, apellido_paterno = %s, contrasena = %s, tipo = %s,area = %s WHERE ID = %s"
            cursor.execute(sql, (username, nombre, apellido_materno, apellido_paterno, hashed_password, gender,area,user_id))
            conn.commit()

        flash('Usuario actualizado con éxito.')
        return redirect(url_for('home.Admin'))

    # Rellenar el formulario con los datos del usuario a actualizar
    form.username.data = user['username']
    form.nombre.data = user['nombre']
    form.apellido_materno.data = user['apellido_materno']
    form.apellido_paterno.data = user['apellido_paterno']
    form.gender.data = user['tipo']
    form.area.data = user['area']

    return render_template('auth/update.html', form=form, user=user)


@home_blueprint.route('/user')
@login_required
def user():
    # Obtén el ID del usuario que ha iniciado sesión
    user_id = current_user.id

    # Crear un cursor
    conn = get_connection()
    with conn.cursor() as cursor:
        # Ejecutar una consulta para seleccionar los datos del usuario que ha iniciado sesión
        sql = "SELECT * FROM Usuario WHERE ID = %s"
        cursor.execute(sql, (user_id,))
        
        # Recuperar el resultado
        usuario = cursor.fetchone()

        # Cerrar el cursor
        cursor.close()

        # Renderizar la plantilla HTML con los datos del usuario
        return render_template('auth/user.html', usuarios=[usuario])

