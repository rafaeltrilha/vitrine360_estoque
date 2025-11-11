from db.connection import conectar

def cadastrar_produto(produto):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO produtos (nome, fabricante, modelo, descricao, quantidade)
        VALUES (%s, %s, %s, %s, %s)
    """, (produto.nome, produto.fabricante, produto.modelo, produto.descricao, produto.quantidade))
    conn.commit()
    registrar_movimentacao(cursor.lastrowid, "entrada", produto.quantidade)
    conn.close()

def baixar_estoque(produto_id, quantidade_baixa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT quantidade FROM produtos WHERE id = %s", (produto_id,))
    resultado = cursor.fetchone()

    if resultado:
        nova_qtd = resultado[0] - quantidade_baixa
        if nova_qtd < 0:
            conn.close()
            return "Estoque insuficiente"
        cursor.execute("UPDATE produtos SET quantidade = %s WHERE id = %s", (nova_qtd, produto_id))
        registrar_movimentacao(produto_id, "baixa", quantidade_baixa)
        conn.commit()
        conn.close()
        return nova_qtd
    conn.close()
    return "Produto não encontrado"

def registrar_movimentacao(produto_id, tipo, quantidade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO movimentacoes (produto_id, tipo, quantidade)
        VALUES (%s, %s, %s)
    """, (produto_id, tipo, quantidade))
    conn.commit()
    conn.close()