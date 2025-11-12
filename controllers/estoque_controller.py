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
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Inicia transação
        cursor.execute("START TRANSACTION")

        # Verifica quantidade atual
        cursor.execute("SELECT quantidade FROM produtos WHERE id = %s FOR UPDATE", (produto_id,))
        resultado = cursor.fetchone()

        if resultado:
            quantidade_atual = resultado[0]
            nova_qtd = quantidade_atual - quantidade_baixa

            if nova_qtd < 0:
                conn.rollback()
                conn.close()
                return "Estoque insuficiente"

            # Atualiza estoque
            cursor.execute("UPDATE produtos SET quantidade = %s WHERE id = %s", (nova_qtd, produto_id))

            # Registra movimentação
            cursor.execute("""
                INSERT INTO movimentacoes (produto_id, tipo, quantidade)
                VALUES (%s, %s, %s)
            """, (produto_id, "baixa", quantidade_baixa))

            conn.commit()
            conn.close()
            return nova_qtd
        else:
            conn.rollback()
            conn.close()
            return "Produto não encontrado"
    except Exception as e:
        try:
            conn.rollback()
            conn.close()
        except:
            pass
        return f"Erro: {str(e)}"

def registrar_movimentacao(produto_id, tipo, quantidade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO movimentacoes (produto_id, tipo, quantidade)
        VALUES (%s, %s, %s)
    """, (produto_id, tipo, quantidade))
    conn.commit()
    conn.close()