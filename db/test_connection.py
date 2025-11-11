from connection import conectar

try:
    conn = conectar()
    print("Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print("Erro na conexão:", e)