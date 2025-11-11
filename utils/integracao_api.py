import requests

def enviar_para_loja(produto):
    url = "https://sualoja.com/api/produtos"  # substitua pela URL real da sua loja
    payload = {
        "nome": produto.nome,
        "fabricante": produto.fabricante,
        "modelo": produto.modelo,
        "descricao": produto.descricao,
        "quantidade": produto.quantidade
    }
    try:
        response = requests.post(url, json=payload)
        return response.status_code == 201
    except Exception as e:
        print("Erro ao enviar para loja:", e)
        return False