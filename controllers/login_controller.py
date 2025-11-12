from db.connection import conectar

def autenticar_usuario(nome, senha):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nome = %s AND senha = %s", (nome, senha))
        usuario = cursor.fetchone()
        conn.close()
        return usuario
    except Exception as e:
        return None