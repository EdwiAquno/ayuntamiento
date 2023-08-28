import pymysql

def get_connection():
    connection = pymysql.connect(host='localhost',
                                 user='ayuntamiento',
                                 password='bigtime19',
                                 db='ayuntamiento',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection