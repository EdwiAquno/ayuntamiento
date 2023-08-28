from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, 
                    SubmitField, EmailField, ValidationError, SelectField, IntegerField, TextAreaField,SelectMultipleField,validators,DateField)
from wtforms.validators import DataRequired, Email, EqualTo, Length

from wtforms.validators import DataRequired, Length

#from .models import  get_user_by_username

from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, 
                    SubmitField, EmailField, ValidationError, SelectField, IntegerField, TextAreaField)
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import  get_user_by_username

from flask_sqlalchemy import SQLAlchemy
from db.db_connection import get_connection



################# Formularios de WTForms ##################
class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    lote = StringField('Lote', validators=[DataRequired()])
    descripcion = StringField('Descripción')
    unidad_de_medida = StringField('Unidad de Medida')
    cantidad_disponible = IntegerField('Cantidad Disponible')
    fecha = DateField('Fecha de registro', validators=[DataRequired()], format='%Y-%m-%d')
    
    area = SelectField('ID Area', coerce=int)
    
    submit = SubmitField('Guardar')
class ProductoeditarForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    lote = StringField('Lote', validators=[DataRequired()])
    descripcion = StringField('Descripción')
    unidad_de_medida = StringField('Unidad de Medida')
    cantidad_disponible = IntegerField('Cantidad Disponible')
    
    area = SelectField('ID Area', coerce=int)
    
    submit = SubmitField('Guardar')
class AreaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción')
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired(), EqualTo('confirm_password', message='Las contraseñas no coinciden')])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired()])
    submit = SubmitField('Guardar')  

class AreaeditarForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción')
    
    submit = SubmitField('Guardar')  


from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class SolicitudForm(FlaskForm):
    descripcion = TextAreaField('Descripción de la solicitud', validators=[DataRequired()])
    numero = StringField('Número de requisición', validators=[DataRequired()])
    usuario_nombre_completo = StringField('Nombre completo del usuario', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    unidad = StringField('Material', validators=[DataRequired()])
    medida = StringField('Unidad de Medida', validators=[DataRequired()])
    submit = SubmitField('Guardar en BDD')
    submit = SubmitField('Agregar Material')
class AceptadasForm(FlaskForm):
    fecha_solicitud = DateField("Fecha de Solicitud", validators=[DataRequired()])
    area_solicitante = StringField("Área Solicitante", validators=[DataRequired()])
    descripcion = TextAreaField("Descripción", validators=[DataRequired()])
    usuario_solicitante = StringField("Usuario Solicitante", validators=[DataRequired()])
    material = SelectField('Material', choices=[], coerce=int)
    numero_requisicion = StringField("Número de Requisición", validators=[DataRequired()])
    unidad_de_medida = StringField("Unidad de Medida", validators=[DataRequired()])
    cantidad = IntegerField("Cantidad", validators=[DataRequired()])
    numero_peticion = StringField("Número de Petición", validators=[DataRequired()])
    concepto = StringField("Concepto", validators=[DataRequired()])
    responsable_aprobacion = StringField("Responsable Aprobación", validators=[DataRequired()])
    submit = SubmitField("Guardar")
    submit = SubmitField('Agregar Material')

class ReportForm(FlaskForm):
    gender = SelectField('Tipo', choices=[('Direccion', 'Direccion'), ('Area', 'Area'), ('Administrador', 'Administrador')], validators=[DataRequired()])
    fecha_aprobacion = SelectField('Fecha de Aprobación')


class LlenarTablaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    direccion = StringField('Dirección', validators=[DataRequired()])
    ciudad = StringField('Ciudad', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    correo_electronico = StringField('Correo Electrónico', validators=[DataRequired()])
    submit = SubmitField('Guardar')
class LlenarTablaeditarForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    direccion = StringField('Dirección', validators=[DataRequired()])
    ciudad = StringField('Ciudad', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    correo_electronico = StringField('Correo Electrónico', validators=[DataRequired()])
    submit = SubmitField('Guardar')