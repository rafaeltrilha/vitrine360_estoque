def verificar_alerta(qtd):
    if qtd < 5:
        return f"⚠️ Estoque baixo: apenas {qtd} unidades restantes!"
    return None