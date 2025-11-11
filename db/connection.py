import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="rafael",
        password="Aline@2001",
        database="vitrine360"
    )