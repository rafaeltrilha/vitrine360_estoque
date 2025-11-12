from db.connection import conectar

def autenticar(nome, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nome = %s AND senha = %s", (nome, senha))
    usuario = cursor.fetchone()
    conn.close()
    return usuario