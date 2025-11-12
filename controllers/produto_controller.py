from db.connection import conectar

def cadastrar_produto(nome, fabricante, modelo, descricao, quantidade):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO produtos (nome, fabricante, modelo, descricao, quantidade)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome, fabricante, modelo, descricao, int(quantidade)))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Erro ao cadastrar produto:", e)