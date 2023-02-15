#FALTA HACER

import pyodbc

def create_connection(database, server='localhost\\sqlexpress', username="localhost\\Usuario", password=""):
    connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor

def close_connection(connection):
    connection.close()