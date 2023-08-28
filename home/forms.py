from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, 
                    SubmitField, EmailField, ValidationError, SelectField, IntegerField, TextAreaField)
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import  get_user_by_username

from flask_sqlalchemy import SQLAlchemy
from db.db_connection import get_connection


################# Formularios de WTForms ##################
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Ingresar')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Email

def get_user_by_email(email):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM Usuario WHERE email = %s"
        cursor.execute(sql, (email,))
        user = cursor.fetchone()
    return user



class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=3, max=50)])
    apellido_paterno = StringField('Apellido Paterno', validators=[DataRequired(), Length(min=3, max=50)])
    apellido_materno = StringField('Apellido Materno', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    gender = SelectField('Tipo', choices=[('Direccion', 'Direccion'), ('Area', 'Area'), ('Administrador', 'Administrador')], validators=[DataRequired()])
    area = SelectField('Area', validators=[DataRequired()])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

class UpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=3, max=50)])
    apellido_paterno = StringField('Apellido Paterno', validators=[DataRequired(), Length(min=3, max=50)])
    apellido_materno = StringField('Apellido Materno', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    gender = SelectField('Tipo', choices=[('Direccion', 'Direccion'), ('Area', 'Area'), ('Administrador', 'Administrador')], validators=[DataRequired()])
    area = SelectField('Area', validators=[DataRequired()])
    submit = SubmitField('Actualizar')

    ######## Validar Correo Unico #########
    def validate_email(self, field):
        ######## Consultar si el correo existe en la base de datos #######
        if get_user_by_email(field.data):
            raise ValidationError('El correo ya existe')

    ######## Validar Username Unico #########
    def validate_username(self, field):
        ######## Consultar si el username existe en la base de datos #######
        if get_user_by_username(field.data):
            raise ValidationError('El username ya existe')

########### TODO: Formularios de Profile ###########
class ProfileForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    last_name = StringField('Apellidos', validators=[DataRequired()])
    #phone = IntegerField('Teléfono')
    #is_married = RadioField('Estado Civil', choices=[('True', 'Casado'), ('False', 'Soltero')])
    #gender = SelectField('Genero', choices=[('male', 'Masculino'), ('female', 'Femenino'), ('other', 'Otro')])
#class AlumnosInformacion(db.Model):
 #   __tablename__ = 'alumnos_informacion'
  #  nombre = db.Column(db.String(50), primary_key=True)
   # matricula = db.Column(db.String(10))
   # nombre_grado = db.Column(db.String(20))
   # nombre_grupo = db.Column(db.String(10))
    #nombre_carrera = db.Column(db.String(50))


