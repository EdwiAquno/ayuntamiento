from flask_login import UserMixin
from db.db_connection import get_connection
from werkzeug.security import check_password_hash

class User(UserMixin):

    
    def __init__(self, id, username, tipo_usuario, area):
        self.id = id
        self.username = username
        self.tipo = tipo_usuario
        self.area = area


def get_user_by_id(id):
    ####### Consultar en BD por id
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = f"SELECT * FROM Usuario WHERE ID = '{id}'"
        cursor.execute(sql)
        user = cursor.fetchone()
        if user:
            return User(user['ID'], user['nombre'],  user['tipo'], user['area'])
        else:
            return None

def get_user_by_username_and_password(username, password):
    ####### Consultamos user por username ##########
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = f"SELECT * FROM Usuario WHERE nombre = '{username}'"
        cursor.execute(sql)
        user = cursor.fetchone()
        if user:
            ####### Comparamos password #######
            if check_password_hash(user['contrasena'], password):
                return User(user['ID'], user['nombre'], user['tipo'], user['area'])
            else:
                return None
        else:
            return None



def get_user_by_username(username):
    ####### Cosultar en BD por username
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = f"SELECT * FROM Usuario WHERE nombre = '{username}'"
        cursor.execute(sql)
        user = cursor.fetchone()
        if user:
            return User(user['ID'], user['nombre'], user['tipo'], user['area'])
        else:
            return None